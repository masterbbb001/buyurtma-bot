# Menyu ma'lumotlari
# Har bir taomda: id, nomi, narxi (so'm), tavsifi, emoji

MENU = {
    "salqin": {
        "name": "🧊 Salqin Ichimliklar",
        "items": [
            {
                "id": "s1",
                "name": "Coca-Cola 0.5L",
                "price": 8000,
                "desc": "Sovuq Coca-Cola, muzli 🧊",
                "emoji": "🥤",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Cocacola_can.png/220px-Cocacola_can.png"
            },
            {
                "id": "s2",
                "name": "Sprite 0.5L",
                "price": 7000,
                "desc": "Limon-limon ta'mli sovuq Sprite 🍋",
                "emoji": "🥤",
                "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Sprite_2022.png/220px-Sprite_2022.png"
            },
            {
                "id": "s3",
                "name": "Lipton Choy",
                "price": 6000,
                "desc": "Sovuq shirin muzli choy 🍵",
                "emoji": "🧃",
                "photo": None
            },
            {
                "id": "s4",
                "name": "Toza Suv 0.5L",
                "price": 3000,
                "desc": "Toza ichimlik suvi 💧",
                "emoji": "💧",
                "photo": None
            },
            {
                "id": "s5",
                "name": "Freshly Limonadi",
                "price": 12000,
                "desc": "Yangi siqilgan limon bilan tayyorlangan tabiiy limonad 🍋",
                "emoji": "🍹",
                "photo": None
            },
        ]
    },
    "milliy": {
        "name": "🍽️ Milliy Taomlar",
        "items": [
            {
                "id": "m1",
                "name": "Osh (Palov)",
                "price": 25000,
                "desc": "Paxta moyi va qo'y go'shtidan tayyorlangan haqiqiy o'zbek palovi 🌾",
                "emoji": "🍛",
                "photo": None
            },
            {
                "id": "m2",
                "name": "Lag'mon",
                "price": 22000,
                "desc": "Qo'lda cho'zilgan qo'shimcha bilan mol go'shti va sabzavotlar 🍜",
                "emoji": "🍜",
                "photo": None
            },
            {
                "id": "m3",
                "name": "Manti",
                "price": 20000,
                "desc": "Bug'da pishirilgan qo'y go'shtli manti, qatiq bilan ✨",
                "emoji": "🥟",
                "photo": None
            },
            {
                "id": "m4",
                "name": "Shurva",
                "price": 18000,
                "desc": "Issiq qo'y go'shtli shurva, non bilan 🥣",
                "emoji": "🍲",
                "photo": None
            },
            {
                "id": "m5",
                "name": "Somsa (2 dona)",
                "price": 12000,
                "desc": "Tandirda pishirilgan go'shtli somsa 🫓",
                "emoji": "🥐",
                "photo": None
            },
        ]
    },
    "fastfood": {
        "name": "🍔 Fast Food",
        "items": [
            {
                "id": "f1",
                "name": "Katta Burger",
                "price": 35000,
                "desc": "Mol go'shtli katta burger, salat va sous bilan 🥬",
                "emoji": "🍔",
                "photo": None
            },
            {
                "id": "f2",
                "name": "Chicken Burger",
                "price": 30000,
                "desc": "Qovurilgan tovuq go'shtli burger, sous bilan 🍗",
                "emoji": "🍔",
                "photo": None
            },
            {
                "id": "f3",
                "name": "Kartoshka Fri (L)",
                "price": 15000,
                "desc": "Tuzli qovurilgan kartoshka, ketchup bilan 🍟",
                "emoji": "🍟",
                "photo": None
            },
            {
                "id": "f4",
                "name": "Hot-Dog",
                "price": 18000,
                "desc": "Kolbasa, gorchitsa va ketchup bilan hot-dog 🌭",
                "emoji": "🌭",
                "photo": None
            },
            {
                "id": "f5",
                "name": "Pizza (4 bo'lak)",
                "price": 45000,
                "desc": "Margherita yoki pepperoni pizza, issiq holda 🍕",
                "emoji": "🍕",
                "photo": None
            },
        ]
    }
}

def get_item_by_id(item_id: str):
    for category in MENU.values():
        for item in category["items"]:
            if item["id"] == item_id:
                return item
    return None
