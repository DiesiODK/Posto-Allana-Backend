"""Static menu data seeded from the Posto Allana PDF cardápio."""

M = lambda n: f"/menu/{n}.jpg"

# Image pool - fotos reais extraídas do cardápio em PDF
PIZZA1 = M("pizza_1")
PIZZA2 = M("pizza_2")
PIZZA3 = M("pizza_3")
PIZZA4 = M("pizza_1")
PIZZASP = M("pizza_3")
SUSHI1 = M("temaki_1")
SUSHI2 = M("temaki_2")
SUSHI3 = M("temaki_3")
SUSHI4 = M("temaki_4")
SUSHICOMBO = M("combinado_1")
NIGIRI = M("uramaki_2")
CHAPA1 = M("chapa_1")
CHAPA2 = M("chapa_1")
MEAT3 = M("chapa_1")
BATATA = M("porcao_1")
BURGER = M("porcao_1")
DRINK1 = M("drink_1")
DRINK2 = M("drink_2")
JUICE1 = M("sucos")
JUICE2 = M("sucos")
SANDWICH1 = M("lanches")
SANDWICH2 = M("lanches")
SODA = M("bebidas")
BEER = M("bebidas")
DESSERT1 = M("sobremesa_1")
DESSERT2 = M("sobremesa_2")
SHRIMP1 = M("porcao_2")
SHRIMP2 = M("porcao_1")
YAKISOBA = M("yakisoba")

CATEGORIES = [
    {"slug": "pizzas", "label": "Pizzas"},
    {"slug": "pizzas-doces", "label": "Pizzas Doces"},
    {"slug": "bordas", "label": "Bordas"},
    {"slug": "chapas", "label": "Chapas"},
    {"slug": "porcoes", "label": "Porções"},
    {"slug": "entradas", "label": "Entradas"},
    {"slug": "yakisoba", "label": "Yakisoba"},
    {"slug": "temaki", "label": "Temaki"},
    {"slug": "hot-roll", "label": "Hot Roll"},
    {"slug": "niguiri", "label": "Niguiri"},
    {"slug": "uramaki", "label": "Uramaki"},
    {"slug": "hossomaki", "label": "Hossomaki"},
    {"slug": "joe", "label": "Joe"},
    {"slug": "sashimi", "label": "Sashimi"},
    {"slug": "combinados", "label": "Combinados"},
    {"slug": "sobremesa", "label": "Sobremesa"},
    {"slug": "lanches", "label": "Lanches"},
    {"slug": "bebidas", "label": "Bebidas"},
    {"slug": "sucos", "label": "Sucos"},
    {"slug": "drinks", "label": "Drinks"},
    {"slug": "drinks-sem-alcool", "label": "Drinks Sem Álcool"},
]


def _p(code, name, cat, image, desc="", price=None, variants=None):
    return {
        "code": code,
        "name": name,
        "category": cat,
        "image": image,
        "description": desc,
        "price": price,
        "variants": variants or [],
    }


def _v(*pairs):
    return [{"label": l, "price": pr} for l, pr in pairs]


MENU = [
    # PIZZAS
    _p("0001", "Milho", "pizzas", PIZZA1, "Molho, mussarela, milho, catupiry, azeitona e orégano", 47.00),
    _p("0002", "Pan Quatro Queijos", "pizzas", PIZZA4, "Molho, mussarela, parmesão, gorgonzola, catupiry, azeitona e orégano", 50.00),
    _p("0003", "Portuguesa", "pizzas", PIZZA2, "Molho, mussarela, presunto, calabresa, pimentão, cebola, ovo, azeitona e orégano", 47.00),
    _p("0004", "Pepperoni", "pizzas", PIZZA3, "Molho, mussarela, pepperoni, cebola, azeitona e orégano", 50.00),
    _p("0005", "Portuguesa Especial", "pizzas", PIZZASP, "Molho, mussarela, presunto, bacon, ovo, ervilha, cebola, azeitona e orégano", 50.00),
    _p("0006", "Presunto ao Bacon", "pizzas", PIZZA1, "Molho, mussarela, presunto, bacon, ovo, catupiry, azeitona e orégano", 50.00),
    _p("0007", "Mussarela", "pizzas", PIZZA2, "Molho, mussarela, tomate fatiado, azeitona e orégano", 47.00),
    _p("0008", "Americana", "pizzas", PIZZA3, "Molho, mussarela, presunto, bacon, ovo, palmito picado, ervilha, azeitona e orégano", 50.00),
    _p("0009", "Atum", "pizzas", PIZZA4, "Molho, mussarela, atum, tomate fatiado, cebola, azeitona e orégano", 55.00),
    _p("0010", "Brócolis com Palmito", "pizzas", PIZZASP, "Molho, mussarela, brócolis, palmito picado, bacon, catupiry, azeitona e orégano", 55.00),
    _p("0011", "Calabresa", "pizzas", PIZZA3, "Molho, mussarela, calabresa, cebola, azeitona e orégano", 47.00),
    _p("0012", "Nordestina", "pizzas", PIZZA1, "Molho, mussarela, carne seca, cebola, azeitona e orégano", 50.00),
    _p("0013", "Frango com Catupiry", "pizzas", PIZZA2, "Molho, mussarela, frango, catupiry, azeitona e orégano", 50.00),
    # PIZZAS DOCES
    _p("1001", "Brigadeiro", "pizzas-doces", DESSERT1, "Chocolate derretido e granulado", 47.00),
    _p("1002", "M&M", "pizzas-doces", DESSERT2, "Chocolate derretido e M&M", 50.00),
    _p("1003", "Banana Suprema", "pizzas-doces", DESSERT1, "Mussarela, chocolate e banana", 47.00),
    # BORDAS
    _p("001", "Borda Chocolate ao Leite", "bordas", PIZZA4, "Borda recheada", 8.00),
    _p("002", "Borda Catupiry", "bordas", PIZZA4, "Borda recheada", 8.00),
    _p("003", "Borda Cheddar", "bordas", PIZZA4, "Borda recheada", 8.00),
    _p("004", "Borda Cream Cheese", "bordas", PIZZA4, "Borda recheada", 8.00),
    _p("005", "Borda Mussarela", "bordas", PIZZA4, "Borda recheada", 8.00),
    # CHAPAS
    _p("2001", "Chapa Aditivada", "chapas", CHAPA1, "Picanha acebolada, anéis de cebola, calabresa, batata frita e porção de arroz", 99.90),
    _p("2002", "Chapa Diesel", "chapas", CHAPA2, "Contrafilé acebolado, anéis de cebola, calabresa, batata frita e porção de arroz", 89.90),
    _p("2003", "Chapa S10", "chapas", MEAT3, "Frango empanado, anéis de cebola, calabresa, batata frita e porção de arroz", 79.90),
    _p("2004", "Chapa da Casa", "chapas", CHAPA1, "Contrafilé, frango acebolado, calabresa, batata frita (ou mandioca frita) e porção de arroz", 85.90),
    # PORÇÕES
    _p("3001", "Picanha Acebolada + Batata Frita", "porcoes", MEAT3, "", 82.90),
    _p("3002", "Contrafilé Acebolado + Batata Frita", "porcoes", CHAPA2, "", 74.90),
    _p("3003", "Calabresa Acebolada + Batata Frita", "porcoes", CHAPA1, "", 58.90),
    _p("3004", "Filé de Frango Acebolado + Batata Frita", "porcoes", SHRIMP1, "", 58.90),
    _p("3005", "Isca de Frango Empanado", "porcoes", SHRIMP2, "", 48.90),
    _p("3006", "Isca de Tilápia Empanada", "porcoes", SHRIMP2, "", 46.90),
    _p("3007", "Manjubinha", "porcoes", SHRIMP1, "", 20.90),
    _p("3008", "Frango à Passarinho + Batata Frita", "porcoes", BATATA, "", 49.90),
    _p("3009", "Camarão Empanado", "porcoes", SHRIMP2, "", 72.90),
    _p("3010", "Camarão Alho e Óleo", "porcoes", SHRIMP1, "", 72.90),
    _p("3011", "Batata Frita", "porcoes", BATATA, "", 21.90),
    _p("3012", "Mini Pastel de Queijo (8 unidades)", "porcoes", BURGER, "", 19.90),
    _p("3013", "Mini Salgados (12 unidades)", "porcoes", BURGER, "", 19.90),
    _p("3014", "Arroz", "porcoes", BATATA, "", 5.99),
    # ENTRADAS
    _p("4001", "Bolinha de Salmão à Milanesa", "entradas", SHRIMP2, "10 unidades", 28.50),
    _p("4002", "Ceviche Salmão", "entradas", SUSHI3, "200g", 24.90),
    _p("4003", "Carpaccio Salmão", "entradas", SUSHI4, "200g", 26.90),
    _p("4004", "Harumaki", "entradas", SHRIMP1, "Queijo, legumes ou goiabada com queijo", None, _v(("01 und", 3.90), ("03 und", 9.00))),
    _p("4005", "Harumaki Camarão", "entradas", SHRIMP2, "Camarão com cream cheese", None, _v(("01 und", 5.90), ("03 und", 15.00))),
    # YAKISOBA
    _p("5001", "Yakisoba Tradicional", "yakisoba", YAKISOBA, "Macarrão, legume, carne e frango", None, _v(("1 porção", 22.50), ("2 porções", 34.90))),
    _p("5002", "Yakisoba Camarão Especial", "yakisoba", YAKISOBA, "Macarrão, camarão, legume, carne e frango", None, _v(("1 porção", 24.90), ("2 porções", 38.90))),
    # TEMAKI
    _p("6001", "Temaki Filadélfia", "temaki", SUSHI1, "Salmão cru, cream cheese e cebolinha", 19.90),
    _p("6002", "Temaki Nachos", "temaki", SUSHI2, "Salmão cru, doritos, cream cheese e cebolinha", 20.50),
    _p("6003", "Temaki Salmão Grelhado", "temaki", SUSHI3, "Salmão grelhado, cream cheese e cebolinha", 20.50),
    _p("6004", "Temaki Salmão Empanado", "temaki", SUSHI4, "Salmão empanado, cream cheese e cebolinha", 20.50),
    _p("6005", "Temaki Hot", "temaki", SUSHI1, "Temaki empanado, salmão grelhado, cream cheese", 20.90),
    _p("6006", "Temaki Camarão", "temaki", SUSHI2, "Camarão (empanado ou pré-cozido), cream cheese e cebolinha", 20.90),
    _p("6007", "Temaki California", "temaki", SUSHI3, "Pepino, manga e kani", 18.90),
    _p("6008", "Big Temaki", "temaki", SUSHI4, "Salmão cru ou grelhado, cream cheese e cebolinha", 29.90),
    _p("6009", "Temaki Filadélfia (sem arroz)", "temaki", SUSHI1, "Salmão cru, cream cheese e cebolinha", 32.90),
    _p("6010", "Temaki Hot (sem arroz)", "temaki", SUSHI2, "Temaki empanado, salmão grelhado, cream cheese", 42.90),
    # HOT ROLL
    _p("7001", "Hot Maki", "hot-roll", SUSHI3, "Salmão, cream cheese e cebolinha (10 und)", 18.90),
    _p("7002", "Hot Salmão", "hot-roll", SUSHI4, "Salmão enrolado, sem arroz, cream cheese e cebolinha (10 und)", 22.90),
    _p("7003", "Hot Ebi", "hot-roll", SUSHI1, "Camarão, cream cheese e cebolinha (10 und)", 20.50),
    _p("7004", "Hot Luisinho", "hot-roll", SUSHI2, "Salmão cru em cima, cream cheese, cebolinha e raspas de limão (10 und)", 20.50),
    _p("7005", "Big Hot", "hot-roll", SUSHI3, "Salmão (cru ou grelhado), cream cheese, cebolinha (10 und)", 26.90),
    _p("7006", "Hot do Posto", "hot-roll", SUSHI4, "Salmão, cream cheese e cebolinha c/ 3 recheios em cima (10 und)", 20.50),
    # NIGUIRI
    _p("8001", "Niguiri Salmão", "niguiri", NIGIRI, "", None, _v(("06 und", 16.50), ("10 und", 26.50))),
    _p("8002", "Niguiri Salmão Maçaricado", "niguiri", NIGIRI, "", None, _v(("06 und", 18.50), ("10 und", 28.50))),
    _p("8003", "Niguiri Premium", "niguiri", NIGIRI, "", None, _v(("06 und", 21.90), ("10 und", 29.90))),
    # URAMAKI
    _p("9001", "Uramaki Filadélfia", "uramaki", SUSHI1, "Salmão cru, cream cheese e cebolinha (10 und)", 19.90),
    _p("9002", "Uramaki Salmão Grelhado", "uramaki", SUSHI2, "Salmão grelhado, cream cheese e cebolinha (10 und)", 19.90),
    _p("9003", "Uranachos", "uramaki", SUSHI3, "Salmão cru, cream cheese, cebolinha e doritos (10 und)", 20.90),
    _p("9004", "Uramaki Ebi", "uramaki", SUSHI4, "Camarão (empanado ou pré-cozido), cream cheese e cebolinha (10 und)", 19.90),
    _p("9005", "Uramaki Salmão Lemon", "uramaki", SUSHI1, "Salmão cru, cream cheese, cebolinha e raspas de limão (10 und)", 18.90),
    _p("9006", "Uramaki Fruta", "uramaki", DESSERT1, "Morango com chocolate (10 und)", 17.90),
    _p("9007", "Uramaki Skin", "uramaki", SUSHI2, "Pele de salmão grelhado, cream cheese e cebolinha (10 und)", 18.90),
    _p("9008", "Uramaki California", "uramaki", SUSHI3, "Pepino, manga e kani (10 und)", 20.90),
    _p("9009", "Uramaki Baterá", "uramaki", SUSHI4, "Salmão cru, cream cheese e alho poró (10 und)", 22.90),
    # HOSSOMAKI
    _p("1101", "Hossomaki Salmão", "hossomaki", SUSHI1, "08 unidades", 15.90),
    _p("1102", "Hossomaki Pepino", "hossomaki", SUSHI2, "08 unidades", 11.90),
    _p("1103", "Hossomaki Kani", "hossomaki", SUSHI3, "08 unidades", 12.90),
    # JOE
    _p("1201", "Joe Salmão Cru", "joe", SUSHI1, "Arroz, salmão, cream cheese e cebolinha", None, _v(("06 und", 16.90), ("10 und", 25.90))),
    _p("1202", "Joe Salmão Maçaricado", "joe", SUSHI2, "Arroz, salmão, cream cheese e cebolinha", None, _v(("06 und", 17.90), ("10 und", 27.90))),
    _p("1203", "Joe Camarão", "joe", SUSHI3, "Arroz, camarão, cream cheese e cebolinha", None, _v(("06 und", 18.90), ("10 und", 28.90))),
    _p("1204", "Joe Pepino", "joe", SUSHI4, "Arroz, pepino, salmão, cream cheese e cebolinha", None, _v(("06 und", 10.50), ("10 und", 18.90))),
    _p("1205", "Joe Crispy", "joe", SUSHI1, "Salmão, cream cheese e couve crispy", None, _v(("06 und", 16.90), ("10 und", 26.90))),
    _p("1206", "Joe Doritos", "joe", SUSHI2, "Salmão, cream cheese e doritos", None, _v(("06 und", 16.90), ("10 und", 26.90))),
    _p("1207", "Eby Joe", "joe", SUSHI3, "Camarão empanado e frito, cream cheese e cebolinha", None, _v(("06 und", 18.90), ("10 und", 28.90))),
    _p("1208", "Joe Especial", "joe", SUSHI4, "Salmão, cream cheese, pimenta biquinho e cebolinha", None, _v(("06 und", 16.90), ("10 und", 26.90))),
    # SASHIMI
    _p("1301", "Sashimi Salmão", "sashimi", SUSHI3, "", None, _v(("08 und", 28.90), ("15 und", 49.90))),
    _p("1302", "Sashimi Salmão Premium", "sashimi", SUSHI4, "", None, _v(("08 und", 32.90), ("15 und", 54.90))),
    # COMBINADOS
    _p("1401", "Combo Grelhado 1", "combinados", SUSHICOMBO, "1 temaki hot de salmão, 4 uramaki salmão grelhado, 2 luizinho maçaricado, 2 niguiri maçaricado", 32.90),
    _p("1402", "Combo Individual", "combinados", SUSHICOMBO, "10 hot roll, 4 hossomaki, 4 uramaki, 2 niguiri, 2 luizinhos", 38.90),
    _p("1403", "Combo Premium", "combinados", SUSHICOMBO, "10 hot roll, 10 uramaki baterá, 2 niguiri, 2 luizinho de salmão e 1 temaki hot", 54.90),
    _p("1404", "Combo Cocal", "combinados", SUSHICOMBO, "6 sashimis, 8 hossomaki, 6 niguiris e 4 luizinhos", 58.90),
    _p("1405", "Combo Grelhado 2", "combinados", SUSHICOMBO, "2 temaki hot de salmão, 10 uramaki grelhado, 4 luizinho maçaricado, 4 niguiri, 2 harumaki", 62.90),
    _p("1406", "Combo Posto", "combinados", SUSHICOMBO, "10 sashimis, 6 niguiris, 8 hossomaki, 10 uramaki e 4 luizinhos", 79.90),
    _p("1407", "Combo Especial", "combinados", SUSHICOMBO, "15 sashimis, 8 hossomaki, 10 uramaki, 6 niguiri, 4 luizinhos, 2 temaki e 10 hot roll", 120.00),
    _p("1408", "Combo Favorito", "combinados", SUSHICOMBO, "8 sashimis, 8 hot roll, 8 uramaki", 64.90),
    _p("1409", "Combo Clássico", "combinados", SUSHICOMBO, "1 temaki filadélfia, 8 uramaki, 8 hot roll, 8 hossomaki", 58.90),
    # SOBREMESA
    _p("1501", "Temaki Doce", "sobremesa", DESSERT1, "Morango ou banana com nutella", 22.90),
    _p("1502", "Joe Goiabada", "sobremesa", DESSERT2, "Goiaba com chocolate e morango (8 und)", 18.50),
    _p("1503", "Hot Doce", "sobremesa", DESSERT1, "Morango ou banana com chocolate e leite condensado (10 und)", 18.90),
    # LANCHES
    _p("1601", "Lanche Filé de Frango", "lanches", SANDWICH1, "Pão baguete, filé de frango, presunto, queijo e salada", 23.90),
    _p("1602", "Churrasco Contrafilé", "lanches", SANDWICH2, "Pão baguete, contrafilé, presunto, queijo, ovo e salada", 28.90),
    _p("1603", "Lanche Posto Allana", "lanches", SANDWICH1, "Pão baguete, calabresa e queijo", 21.90),
    # BEBIDAS
    _p("B01", "Água Mineral sem Gás", "bebidas", SODA, "", 4.00),
    _p("B02", "Água Mineral com Gás", "bebidas", SODA, "", 5.00),
    _p("B03", "Cerveja Long Neck", "bebidas", BEER, "", 12.00),
    _p("B04", "Refrigerante Lata", "bebidas", SODA, "", 6.00),
    _p("B05", "H2O", "bebidas", SODA, "", 7.00),
    # SUCOS
    _p("1801", "Suco de Acerola", "sucos", JUICE2, "", 7.90),
    _p("1802", "Suco de Morango", "sucos", JUICE2, "", 7.90),
    _p("1803", "Suco de Abacaxi", "sucos", JUICE1, "", 7.90),
    _p("1804", "Suco de Limão", "sucos", JUICE1, "", 7.90),
    _p("1805", "Suco de Maracujá", "sucos", JUICE1, "", 7.90),
    _p("1806", "Suco de Abacaxi c/ Hortelã", "sucos", JUICE2, "", 7.90),
    _p("1807", "Suco de Laranja", "sucos", JUICE1, "", 9.50),
    # DRINKS
    _p("1901", "Combo Gin", "drinks", DRINK1, "1 Tanqueray 750ml, 4 Red Bulls e gelo", 190.90),
    _p("1902", "Combo Whisky", "drinks", DRINK2, "1 Whisky (Old Parr, Black White, Red Label ou Black Label), 4 Red Bulls e gelo", 210.00),
    _p("1903", "Gin Tônica", "drinks", DRINK1, "Gin, água tônica e toque de limão", 24.90),
    _p("1904", "Gin Tropical", "drinks", DRINK1, "Gin, energético tropical e toque de limão", 24.90),
    _p("1905", "Gin Melancia", "drinks", DRINK1, "Gin, energético de melancia e toque de limão", 24.90),
    _p("1906", "Gin Tônica Blue", "drinks", DRINK2, "Gin, água tônica, licor de laranja azul e toque de limão", 24.90),
    _p("1907", "Caipiroska Morango", "drinks", DRINK2, "Vodka, morango e açúcar", 19.90),
    _p("1908", "Caipiroska Maracujá", "drinks", DRINK2, "Vodka, polpa de maracujá e açúcar", 19.90),
    _p("1909", "Caipiroska Limão", "drinks", DRINK1, "Vodka, limão e açúcar", 19.90),
    _p("1910", "Caipiroska Kiwi", "drinks", DRINK2, "Vodka, kiwi e açúcar", 19.90),
    _p("1911", "Mojito Allana", "drinks", DRINK1, "Vodka, citrus, xarope de morango, morango, rodelas de limão e açúcar", 20.90),
    _p("1912", "Aperol Spritz", "drinks", DRINK2, "Aperol, espumante, água com gás, rodelas de laranja", 26.90),
    _p("1913", "Sex On The Beach", "drinks", DRINK1, "Vodka, licor de pêssego, suco de laranja, xarope de groselha", 28.90),
    _p("1914", "Espanhola Morango", "drinks", DRINK2, "Vinho tinto, morango, leite condensado", 26.90),
    _p("1915", "Espanhola Maracujá", "drinks", DRINK2, "Vinho tinto, polpa de maracujá, leite condensado", 26.90),
    # DRINKS SEM ÁLCOOL
    _p("2101", "Coquetel de Abacaxi", "drinks-sem-alcool", JUICE1, "", 18.90),
    _p("2102", "Coquetel de Morango", "drinks-sem-alcool", JUICE2, "", 18.90),
    _p("2103", "Coquetel de Frutas Vermelhas", "drinks-sem-alcool", JUICE2, "", 19.90),
    _p("2104", "Milk-Shake", "drinks-sem-alcool", DESSERT1, "Morango, chocolate ou açaí", 16.90),
    _p("2105", "Mojito Allana Sem Álcool", "drinks-sem-alcool", DRINK1, "Citrus, xarope de morango, morango, rodelas de limão e açúcar", 18.90),
    _p("2106", "Soda Italiana", "drinks-sem-alcool", JUICE1, "Morango, maçã verde, limão siciliano, tangerina, groselha", 18.90),
]


# Override por categoria usando as fotos reais do PDF (rotação quando há várias)
CATEGORY_IMAGES = {
    "pizzas": [M("pizza_1"), M("pizza_2"), M("pizza_3")],
    "pizzas-doces": [M("pizza_doce"), M("sobremesa_1")],
    "bordas": [M("pizza_1")],
    "chapas": [M("chapa_1")],
    "porcoes": [M("porcao_1"), M("porcao_2"), M("chapa_1")],
    "entradas": [M("porcao_1"), M("combinado_2"), M("uramaki_2")],
    "yakisoba": [M("yakisoba")],
    "temaki": [M("temaki_1"), M("temaki_2"), M("temaki_3"), M("temaki_4")],
    "hot-roll": [M("hotroll")],
    "niguiri": [M("uramaki_2"), M("combinado_1")],
    "uramaki": [M("uramaki_1"), M("uramaki_2")],
    "hossomaki": [M("hossomaki")],
    "joe": [M("joe")],
    "sashimi": [M("combinado_1"), M("combinado_2")],
    "combinados": [M("combinado_1"), M("combinado_2")],
    "sobremesa": [M("sobremesa_1"), M("sobremesa_2")],
    "lanches": [M("lanches")],
    "bebidas": [M("bebidas")],
    "sucos": [M("sucos")],
    "drinks": [M("drink_1"), M("drink_2"), M("drink_3")],
    "drinks-sem-alcool": [M("drink_3"), M("drink_1"), M("drink_2")],
}

_cat_counter = {}
for _item in MENU:
    _imgs = CATEGORY_IMAGES.get(_item["category"])
    if _imgs:
        _i = _cat_counter.get(_item["category"], 0)
        _item["image"] = _imgs[_i % len(_imgs)]
        _cat_counter[_item["category"]] = _i + 1


def default_hours():
    # 0=Domingo ... 6=Sábado
    base = {"enabled": True, "open": "18:00", "close": "23:30"}
    weekend = {"enabled": True, "open": "18:00", "close": "00:30"}
    return {
        "0": {**base},
        "1": {**base},
        "2": {**base},
        "3": {**base},
        "4": {**base},
        "5": {**weekend},
        "6": {**weekend},
    }


DEFAULT_SETTINGS = {
    "name": "Posto Allana",
    "tagline": "O sabor autêntico de Cocal na sua mesa",
    "address": "Cocal - PI",
    "whatsapp_number": "86994477146",
    "msg_received": "Olá {nome}! 👋 Recebemos o seu pedido no {loja} e já estamos preparando 👨‍🍳🔥. Em breve avisamos quando estiver pronto!",
    "msg_ready": "Olá {nome}! ✅ Seu pedido no {loja} está *pronto*! Já pode retirar no balcão ou está saindo para entrega 🛵. Obrigado pela preferência! 🧡",
    "hours": default_hours(),
}
