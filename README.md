# 🤖 BuyurtmaUz Bot — O'rnatish Qo'llanmasi

## 📁 Fayllar tuzilmasi
```
buyurtma_bot/
├── bot.py           # Asosiy fayl
├── config.py        # Sozlamalar (TOKEN, ADMIN ID va h.k.)
├── handlers.py      # Barcha logika
├── keyboards.py     # Tugmalar
├── menu_data.py     # Taomlar menyusi
├── states.py        # FSM holatlari
└── requirements.txt # Kutubxonalar
```

---

## 🚀 1-QADAM: Tokenni yangilash

1. Telegram'da **@BotFather** ga o'ting
2. `/mybots` → BuyurtmaUz_bot → **API Token** → **Revoke current token**
3. Yangi tokenni nusxalab oling
4. `config.py` faylida `YOUR_NEW_TOKEN_HERE` ni yangi token bilan almashtiring

---

## 🆔 2-QADAM: Admin ID olish

1. Telegram'da **@userinfobot** ga `/start` yuboring
2. U sizning ID raqamingizni beradi (masalan: `987654321`)
3. `config.py` da `ADMIN_ID = 123456789` ni o'zingizning ID ga o'zgartiring

---

## 📢 3-QADAM: Kanal sozlamalari

1. Telegram'da kanal yarating (masalan: `@BuyurtmaUzChannel`)
2. **Botingizni kanalga admin qilib qo'shing**
3. `config.py` da `CHANNEL_ID = "@BuyurtmaUzChannel"` ni o'z kanalingiz bilan almashtiring

---

## 💻 4-QADAM: Botni ishga tushirish

### Mahalliy kompyuterda:
```bash
pip install -r requirements.txt
python bot.py
```

### Railway.app (bepul hosting) da:
1. https://railway.app ga kiring
2. **New Project** → **Deploy from GitHub repo**
3. Fayllarni GitHub ga yuklang
4. Railway avtomatik ishga tushiradi

### Render.com (bepul hosting) da:
1. https://render.com ga kiring
2. **New** → **Web Service**
3. GitHub repo ni ulang
4. **Start Command:** `python bot.py`

---

## 🌐 1,000,000 foydalanuvchi uchun maslahat

**Aiogram 3** async arxitekturasi tufayli bitta server:
- ✅ 10,000+ bir vaqtda ulanish
- ✅ Non-blocking I/O
- ✅ Auto-reconnect

**Production uchun qo'shish kerak:**
- Redis (savatcha ma'lumotlari uchun)
- PostgreSQL (buyurtmalar uchun)
- Webhook rejimida ishlatish (polling o'rniga)

---

## 🎛️ Admin komandalar

| Komanda | Vazifasi |
|---------|----------|
| `/orders` | So'nggi 10 buyurtmani ko'rish |
| `/stats` | Statistika (jami buyurtma, daromad) |

---

## 🍽️ Menyu qo'shish/o'chirish

`menu_data.py` faylida `MENU` lug'atiga yangi taom qo'shing:

```python
{
    "id": "f6",          # Unikal ID
    "name": "Yangi taom",
    "price": 25000,      # So'mda
    "desc": "Tavsif...",
    "emoji": "🍕",
    "photo": None        # Yoki rasm URL
}
```

---

## ✅ Bot imkoniyatlari

- ✅ Kanal a'zoligini tekshirish
- ✅ 3 kategoriya (Salqin, Milliy, Fast Food)
- ✅ Har bir taomda rasm, narx, tavsif
- ✅ + / - tugmalar bilan miqdor tanlash
- ✅ Savatcha tizimi
- ✅ Haqiqiy telefon raqam tekshirish
- ✅ Lokatsiya olish (yolg'on lokatsiyani bloklash)
- ✅ Adminga to'liq buyurtma ma'lumoti
- ✅ Buyurtma holati yangilanishi (Tayyorlanmoqda → Kuryerda → Yakunlandi)
- ✅ Xaridorga har bir holat haqida xabar
- ✅ Admin statistika komandasi
