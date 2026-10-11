from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional

import bcrypt
import jwt
import requests
from bson import ObjectId
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from menu_seed import MENU, CATEGORIES, DEFAULT_SETTINGS

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

JWT_ALGORITHM = "HS256"

# ---------- Object Storage ----------
STORAGE_BASE = (os.environ.get("INTEGRATION_PROXY_URL") or "").strip() or "https://integrations.emergentagent.com"
STORAGE_URL = STORAGE_BASE.rstrip("/") + "/objstore/api/v1/storage"
EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY")
APP_NAME = "posto-allana"
MIME_TYPES = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
    "gif": "image/gif", "webp": "image/webp", "heic": "image/heic", "heif": "image/heif",
}
_storage_key = None


def init_storage(force: bool = False):
    global _storage_key
    if _storage_key and not force:
        return _storage_key
    resp = requests.post(f"{STORAGE_URL}/init", json={"emergent_key": EMERGENT_KEY}, timeout=30)
    resp.raise_for_status()
    _storage_key = resp.json()["storage_key"]
    return _storage_key


def put_object(path: str, data: bytes, content_type: str) -> dict:
    key = init_storage()
    resp = requests.put(
        f"{STORAGE_URL}/objects/{path}",
        headers={"X-Storage-Key": key, "Content-Type": content_type},
        data=data, timeout=120,
    )
    if resp.status_code == 404:
        key = init_storage(force=True)
        resp = requests.put(
            f"{STORAGE_URL}/objects/{path}",
            headers={"X-Storage-Key": key, "Content-Type": content_type},
            data=data, timeout=120,
        )
    resp.raise_for_status()
    return resp.json()


def get_object(path: str):
    key = init_storage()
    resp = requests.get(f"{STORAGE_URL}/objects/{path}", headers={"X-Storage-Key": key}, timeout=60)
    if resp.status_code == 404:
        key = init_storage(force=True)
        resp = requests.get(f"{STORAGE_URL}/objects/{path}", headers={"X-Storage-Key": key}, timeout=60)
    resp.raise_for_status()
    return resp.content, resp.headers.get("Content-Type", "application/octet-stream")


def get_jwt_secret() -> str:
    return os.environ["JWT_SECRET"]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        "type": "access",
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "type": "refresh",
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def set_auth_cookies(response: Response, access: str, refresh: str):
    response.set_cookie("access_token", access, httponly=True, secure=True, samesite="none", max_age=43200, path="/")
    response.set_cookie("refresh_token", refresh, httponly=True, secure=True, samesite="none", max_age=604800, path="/")


async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Token inválido")
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        user["_id"] = str(user["_id"])
        user.pop("password_hash", None)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sessão expirada")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ---------- Models ----------
class LoginInput(BaseModel):
    email: str
    password: str


class Variant(BaseModel):
    label: str
    price: float


class ProductInput(BaseModel):
    code: str = ""
    name: str
    description: str = ""
    category: str
    image: str = ""
    price: Optional[float] = None
    variants: List[Variant] = []
    available: bool = True


class SettingsInput(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    address: Optional[str] = None
    whatsapp_number: Optional[str] = None
    hours: Optional[dict] = None
    msg_received: Optional[str] = None
    msg_ready: Optional[str] = None


class OrderItem(BaseModel):
    name: str
    variantLabel: Optional[str] = None
    qty: int
    price: float


class OrderInput(BaseModel):
    customer: dict
    items: List[OrderItem]
    total: float
    payment: dict
    deliveryType: str = "entrega"


app = FastAPI()
api_router = APIRouter(prefix="/api")


def clean(doc: dict) -> dict:
    doc = dict(doc)
    doc.pop("_id", None)
    return doc


# ---------- Auth ----------
@api_router.post("/auth/login")
async def login(data: LoginInput, response: Response):
    email = data.email.strip().lower()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    uid = str(user["_id"])
    access = create_access_token(uid, email)
    refresh = create_refresh_token(uid)
    set_auth_cookies(response, access, refresh)
    return {"id": uid, "email": email, "name": user.get("name"), "role": user.get("role")}


@api_router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"ok": True}


@api_router.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    return {"id": user["_id"], "email": user["email"], "name": user.get("name"), "role": user.get("role")}


@api_router.post("/auth/refresh")
async def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Sem refresh token")
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    access = create_access_token(str(user["_id"]), user["email"])
    response.set_cookie("access_token", access, httponly=True, secure=True, samesite="none", max_age=43200, path="/")
    return {"ok": True}


# ---------- Public ----------
@api_router.get("/categories")
async def get_categories():
    return CATEGORIES


@api_router.get("/products")
async def get_products():
    docs = await db.products.find().sort("order", 1).to_list(1000)
    return [clean(d) for d in docs]


@api_router.get("/settings")
async def get_settings():
    s = await db.settings.find_one({"key": "main"})
    if not s:
        return DEFAULT_SETTINGS
    return {**DEFAULT_SETTINGS, **clean(s)}


@api_router.post("/orders")
async def create_order(data: OrderInput):
    doc = {
        "id": str(uuid.uuid4()),
        "customer": data.customer,
        "items": [i.model_dump() for i in data.items],
        "total": data.total,
        "payment": data.payment,
        "deliveryType": data.deliveryType,
        "status": "novo",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.orders.insert_one(dict(doc))
    return clean(doc)


# ---------- Admin ----------
@api_router.post("/products")
async def create_product(data: ProductInput, user: dict = Depends(get_current_user)):
    count = await db.products.count_documents({})
    doc = data.model_dump()
    doc["id"] = str(uuid.uuid4())
    doc["order"] = count + 1
    await db.products.insert_one(dict(doc))
    return clean(doc)


@api_router.put("/products/{pid}")
async def update_product(pid: str, data: ProductInput, user: dict = Depends(get_current_user)):
    doc = data.model_dump()
    res = await db.products.update_one({"id": pid}, {"$set": doc})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    updated = await db.products.find_one({"id": pid})
    return clean(updated)


@api_router.delete("/products/{pid}")
async def delete_product(pid: str, user: dict = Depends(get_current_user)):
    res = await db.products.delete_one({"id": pid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"ok": True}


@api_router.put("/settings")
async def update_settings(data: SettingsInput, user: dict = Depends(get_current_user)):
    patch = {k: v for k, v in data.model_dump().items() if v is not None}
    await db.settings.update_one({"key": "main"}, {"$set": patch}, upsert=True)
    s = await db.settings.find_one({"key": "main"})
    return clean(s)


@api_router.get("/orders")
async def list_orders(user: dict = Depends(get_current_user)):
    docs = await db.orders.find().sort("created_at", -1).to_list(500)
    return [clean(d) for d in docs]


@api_router.put("/orders/{oid}/status")
async def update_order_status(oid: str, body: dict, user: dict = Depends(get_current_user)):
    patch = {}
    if "status" in body:
        patch["status"] = body["status"]
    if "done" in body:
        patch["done"] = bool(body["done"])
    if not patch:
        raise HTTPException(status_code=400, detail="Nada para atualizar")
    await db.orders.update_one({"id": oid}, {"$set": patch})
    updated = await db.orders.find_one({"id": oid})
    if not updated:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return clean(updated)


@api_router.delete("/orders")
async def clear_orders(user: dict = Depends(get_current_user)):
    res = await db.orders.delete_many({})
    return {"deleted": res.deleted_count}


@api_router.delete("/orders/{oid}")
async def delete_order(oid: str, user: dict = Depends(get_current_user)):
    res = await db.orders.delete_one({"id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"ok": True}


@api_router.post("/upload")
async def upload_image(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    ext = (file.filename.rsplit(".", 1)[-1] if "." in (file.filename or "") else "jpg").lower()
    content_type = file.content_type or MIME_TYPES.get(ext, "application/octet-stream")
    path = f"{APP_NAME}/products/{uuid.uuid4()}.{ext}"
    data = await file.read()
    try:
        result = put_object(path, data, content_type)
    except Exception as e:
        logger.error("Upload failed: %s", e)
        raise HTTPException(status_code=502, detail="Falha ao enviar a imagem. Tente novamente.")
    await db.files.insert_one({
        "id": str(uuid.uuid4()),
        "storage_path": result["path"],
        "original_filename": file.filename,
        "content_type": content_type,
        "size": result.get("size"),
        "is_deleted": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return {"url": f"/api/files/{result['path']}", "path": result["path"]}


@api_router.get("/files/{path:path}")
async def serve_file(path: str):
    record = await db.files.find_one({"storage_path": path, "is_deleted": False})
    if not record:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    try:
        data, content_type = get_object(path)
    except Exception:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return Response(
        content=data,
        media_type=record.get("content_type", content_type),
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[os.environ.get("FRONTEND_URL", "http://localhost:3000")],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_admin():
    email = os.environ["ADMIN_EMAIL"].strip().lower()
    password = os.environ["ADMIN_PASSWORD"]
    existing = await db.users.find_one({"email": email})
    if existing is None:
        await db.users.insert_one({
            "email": email,
            "password_hash": hash_password(password),
            "name": "Administrador",
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        logger.info("Admin seeded: %s", email)
    elif not verify_password(password, existing["password_hash"]):
        await db.users.update_one({"email": email}, {"$set": {"password_hash": hash_password(password)}})


async def seed_menu():
    if await db.products.count_documents({}) == 0:
        docs = []
        for i, item in enumerate(MENU):
            d = dict(item)
            d["id"] = str(uuid.uuid4())
            d["order"] = i + 1
            d["available"] = True
            docs.append(d)
        await db.products.insert_many(docs)
        logger.info("Seeded %d products", len(docs))
    if await db.settings.find_one({"key": "main"}) is None:
        s = dict(DEFAULT_SETTINGS)
        s["key"] = "main"
        await db.settings.insert_one(s)


@app.on_event("startup")
async def startup():
    await db.users.create_index("email", unique=True)
    await db.products.create_index("id", unique=True)
    try:
        init_storage()
        logger.info("Storage initialized")
    except Exception as e:
        logger.error("Storage init failed: %s", e)
    await seed_admin()
    await seed_menu()


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
