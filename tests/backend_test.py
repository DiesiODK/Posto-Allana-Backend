"""Backend regression tests for Posto Allana menu/order API."""
import os
import pytest
import requests

BASE_URL = os.environ["REACT_APP_BACKEND_URL"].rstrip("/") if os.environ.get("REACT_APP_BACKEND_URL") else "https://pedido-whats.preview.emergentagent.com"
ADMIN_EMAIL = "diesiodk1989@hotmail.com"
ADMIN_PASSWORD = "Admin@123"


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def admin_session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    r = s.post(f"{BASE_URL}/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.status_code == 200, f"Admin login failed: {r.status_code} {r.text}"
    return s


# -------- Public endpoints --------
class TestPublic:
    def test_categories(self, session):
        r = session.get(f"{BASE_URL}/api/categories")
        assert r.status_code == 200
        cats = r.json()
        assert isinstance(cats, list)
        assert len(cats) == 21, f"Expected 21 categories, got {len(cats)}"

    def test_products_seeded(self, session):
        r = session.get(f"{BASE_URL}/api/products")
        assert r.status_code == 200
        products = r.json()
        assert isinstance(products, list)
        assert len(products) >= 135, f"Expected >=135 products, got {len(products)}"
        p = products[0]
        assert "name" in p and "category" in p
        # either price or variants exist
        assert p.get("price") is not None or (p.get("variants") and len(p["variants"]) > 0)

    def test_settings_defaults(self, session):
        r = session.get(f"{BASE_URL}/api/settings")
        assert r.status_code == 200
        s = r.json()
        assert s.get("whatsapp_number") == "86994477146"
        assert "Posto Allana" in (s.get("name") or "")
        hours = s.get("hours") or {}
        assert len(hours) == 7, f"Expected hours for 7 days, got {len(hours)}"


# -------- Auth --------
class TestAuth:
    def test_login_success(self, session):
        r = session.post(f"{BASE_URL}/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert r.status_code == 200
        data = r.json()
        assert data["email"] == ADMIN_EMAIL
        assert data["role"] == "admin"
        # httpOnly cookies set
        cookie_names = [c.name for c in session.cookies]
        assert "access_token" in cookie_names
        assert "refresh_token" in cookie_names

    def test_login_invalid(self, session):
        r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": ADMIN_EMAIL, "password": "wrong"})
        assert r.status_code == 401

    def test_me_requires_auth(self):
        r = requests.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code == 401

    def test_me_with_auth(self, admin_session):
        r = admin_session.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code == 200
        assert r.json()["email"] == ADMIN_EMAIL

    def test_logout(self, admin_session):
        # logout on a separate session so we don't break admin_session
        s = requests.Session()
        s.post(f"{BASE_URL}/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        r = s.post(f"{BASE_URL}/api/auth/logout")
        assert r.status_code == 200
        r2 = s.get(f"{BASE_URL}/api/auth/me")
        assert r2.status_code == 401


# -------- Protected endpoints --------
class TestProtected:
    def test_create_product_requires_auth(self):
        r = requests.post(f"{BASE_URL}/api/products", json={"name": "x", "category": "x"})
        assert r.status_code == 401

    def test_orders_list_requires_auth(self):
        r = requests.get(f"{BASE_URL}/api/orders")
        assert r.status_code == 401

    def test_settings_update_requires_auth(self):
        r = requests.put(f"{BASE_URL}/api/settings", json={"name": "x"})
        assert r.status_code == 401


# -------- Product CRUD --------
class TestProductCRUD:
    created_id = None

    def test_crud_flow(self, admin_session):
        # CREATE
        payload = {
            "code": "TEST_001",
            "name": "TEST_Produto",
            "description": "teste",
            "category": "Bebidas",
            "image": "",
            "price": 9.9,
            "variants": [],
            "available": True,
        }
        r = admin_session.post(f"{BASE_URL}/api/products", json=payload)
        assert r.status_code == 200, r.text
        created = r.json()
        pid = created["id"]
        assert created["name"] == "TEST_Produto"
        assert created["price"] == 9.9

        # verify persisted
        r = admin_session.get(f"{BASE_URL}/api/products")
        assert any(p["id"] == pid for p in r.json())

        # UPDATE price
        payload["price"] = 12.5
        payload["name"] = "TEST_Produto_Updated"
        r = admin_session.put(f"{BASE_URL}/api/products/{pid}", json=payload)
        assert r.status_code == 200
        assert r.json()["price"] == 12.5
        assert r.json()["name"] == "TEST_Produto_Updated"

        # DELETE
        r = admin_session.delete(f"{BASE_URL}/api/products/{pid}")
        assert r.status_code == 200
        # confirm gone
        r = admin_session.get(f"{BASE_URL}/api/products")
        assert not any(p["id"] == pid for p in r.json())


# -------- Settings update --------
class TestSettings:
    def test_update_whatsapp_and_hours(self, admin_session):
        original = admin_session.get(f"{BASE_URL}/api/settings").json()
        orig_wa = original.get("whatsapp_number", "86994477146")

        new_wa = "86999998888"
        new_hours = original.get("hours") or {}
        if new_hours:
            # tweak one day
            first_key = list(new_hours.keys())[0]
            new_hours = dict(new_hours)
            new_hours[first_key] = {"open": "08:00", "close": "22:00", "closed": False}

        r = admin_session.put(
            f"{BASE_URL}/api/settings",
            json={"whatsapp_number": new_wa, "hours": new_hours},
        )
        assert r.status_code == 200
        updated = r.json()
        assert updated["whatsapp_number"] == new_wa

        # persistence check
        r = requests.get(f"{BASE_URL}/api/settings")
        assert r.json()["whatsapp_number"] == new_wa

        # restore
        admin_session.put(f"{BASE_URL}/api/settings", json={"whatsapp_number": orig_wa})


# -------- Orders --------
class TestOrders:
    def test_create_order_no_auth_and_admin_lists(self, admin_session):
        payload = {
            "customer": {"name": "TEST Cliente", "phone": "86999990000", "address": "Rua X", "bairro": "Centro"},
            "items": [{"name": "Coca-Cola", "qty": 2, "price": 7.0}],
            "total": 14.0,
            "payment": {"method": "pix"},
            "deliveryType": "entrega",
        }
        r = requests.post(f"{BASE_URL}/api/orders", json=payload)
        assert r.status_code == 200, r.text
        order = r.json()
        assert order["total"] == 14.0
        assert order["status"] == "novo"
        oid = order["id"]

        # admin can list
        r = admin_session.get(f"{BASE_URL}/api/orders")
        assert r.status_code == 200
        orders = r.json()
        assert any(o["id"] == oid for o in orders)
