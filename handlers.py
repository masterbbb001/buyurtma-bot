import uuid
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import (
    Message, CallbackQuery, Contact, Location
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from config import CHANNEL_ID, ADMIN_ID, ORDERS_CHANNEL_ID
from keyboards import (
    main_menu_kb, category_items_kb, item_detail_kb,
    cart_kb, checkout_confirm_kb, share_contact_kb,
    share_location_kb, admin_order_kb, channel_check_kb
)
from menu_data import MENU, get_item_by_id
from states import OrderStates

router = Router()

# ─── In-memory storage (production uchun Redis yoki DB ishlatish tavsiya etiladi) ───
user_carts = {}       # {user_id: {item_id: qty}}
user_orders = {}      # {order_id: order_data}
user_contacts = {}    # {user_id: phone}
# Message IDs to edit admin messages
order_msg_ids = {}    # {order_id: (chat_id, message_id)}


# ─── KANAL TEKSHIRISH ───────────────────────────────────────────────────────────

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status not in ["left", "kicked"]
    except Exception:
        return False


# ─── START ──────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(bot, user_id)

    if not is_subscribed:
        channel_link = f"https://t.me/{CHANNEL_ID.lstrip('@')}"
        await message.answer(
            f"👋 Salom, <b>{message.from_user.first_name}</b>!\n\n"
            f"🤖 <b>BuyurtmaUz</b> botiga xush kelibsiz!\n\n"
            f"⚠️ Botdan foydalanish uchun avval bizning kanalga a'zo bo'lishingiz kerak:\n\n"
            f"📢 {CHANNEL_ID}\n\n"
            f"A'zo bo'lgach, quyidagi '✅ A'zo bo'ldim' tugmasini bosing:",
            parse_mode="HTML",
            reply_markup=channel_check_kb(channel_link)
        )
        return

    await show_main_menu(message, message.from_user.first_name)


@router.callback_query(F.data == "check_subscription")
async def check_sub_callback(call: CallbackQuery, bot: Bot):
    is_subscribed = await check_subscription(bot, call.from_user.id)
    if is_subscribed:
        await call.message.delete()
        await show_main_menu(call.message, call.from_user.first_name)
    else:
        await call.answer(
            "❌ Siz hali kanalga a'zo bo'lmadingiz! Iltimos, avval a'zo bo'ling.",
            show_alert=True
        )


async def show_main_menu(message: Message, name: str):
    await message.answer(
        f"🏠 <b>Asosiy Menyu</b>\n\n"
        f"Salom, <b>{name}</b>! Nima buyurtma berasiz?\n\n"
        f"🧊 Salqin Ichimliklar\n"
        f"🍽️ Milliy Taomlar\n"
        f"🍔 Fast Food\n\n"
        f"Kategoriyani tanlang 👇",
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )


# ─── BACK TO MENU ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "back_menu")
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text(
        "🏠 <b>Asosiy Menyu</b>\n\nKategoriyani tanlang:",
        parse_mode="HTML"
    )
    await call.message.answer(
        "👇 Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_menu_kb()
    )


# ─── KATEGORIYALAR ──────────────────────────────────────────────────────────────

@router.message(F.text == "🧊 Salqin Ichimliklar")
async def show_salqin(message: Message):
    await message.answer(
        "🧊 <b>Salqin Ichimliklar</b>\n\nQuyidagilardan birini tanlang:",
        parse_mode="HTML",
        reply_markup=category_items_kb("salqin")
    )


@router.message(F.text == "🍽️ Milliy Taomlar")
async def show_milliy(message: Message):
    await message.answer(
        "🍽️ <b>Milliy Taomlar</b>\n\nQuyidagilardan birini tanlang:",
        parse_mode="HTML",
        reply_markup=category_items_kb("milliy")
    )


@router.message(F.text == "🍔 Fast Food")
async def show_fastfood(message: Message):
    await message.answer(
        "🍔 <b>Fast Food</b>\n\nQuyidagilardan birini tanlang:",
        parse_mode="HTML",
        reply_markup=category_items_kb("fastfood")
    )


# ─── TAOM TAFSILOTLARI ───────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("item:"))
async def show_item(call: CallbackQuery):
    item_id = call.data.split(":")[1]
    item = get_item_by_id(item_id)
    if not item:
        await call.answer("Taom topilmadi", show_alert=True)
        return

    text = (
        f"{item['emoji']} <b>{item['name']}</b>\n\n"
        f"📝 {item['desc']}\n\n"
        f"💰 Narxi: <b>{item['price']:,} so'm</b>\n\n"
        f"Nechta buyurtma bermoqchisiz?"
    )
    await call.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=item_detail_kb(item_id, 1)
    )


# ─── MIQDOR O'ZGARTIRISH ─────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("qty_plus:"))
async def qty_plus(call: CallbackQuery):
    _, item_id, qty = call.data.split(":")
    qty = int(qty) + 1
    item = get_item_by_id(item_id)
    text = (
        f"{item['emoji']} <b>{item['name']}</b>\n\n"
        f"📝 {item['desc']}\n\n"
        f"💰 Narxi: <b>{item['price']:,} so'm</b>\n"
        f"💳 Jami: <b>{item['price'] * qty:,} so'm</b>\n\n"
        f"Nechta buyurtma bermoqchisiz?"
    )
    await call.message.edit_text(
        text, parse_mode="HTML",
        reply_markup=item_detail_kb(item_id, qty)
    )


@router.callback_query(F.data.startswith("qty_minus:"))
async def qty_minus(call: CallbackQuery):
    _, item_id, qty = call.data.split(":")
    qty = max(1, int(qty) - 1)
    item = get_item_by_id(item_id)
    text = (
        f"{item['emoji']} <b>{item['name']}</b>\n\n"
        f"📝 {item['desc']}\n\n"
        f"💰 Narxi: <b>{item['price']:,} so'm</b>\n"
        f"💳 Jami: <b>{item['price'] * qty:,} so'm</b>\n\n"
        f"Nechta buyurtma bermoqchisiz?"
    )
    await call.message.edit_text(
        text, parse_mode="HTML",
        reply_markup=item_detail_kb(item_id, qty)
    )


@router.callback_query(F.data.startswith("qty_show:"))
async def qty_show(call: CallbackQuery):
    await call.answer("Miqdorni + yoki - bilan o'zgartiring", show_alert=False)


# ─── SAVATGA QO'SHISH ────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("add_cart:"))
async def add_to_cart(call: CallbackQuery):
    _, item_id, qty = call.data.split(":")
    qty = int(qty)
    user_id = call.from_user.id
    item = get_item_by_id(item_id)

    if user_id not in user_carts:
        user_carts[user_id] = {}

    if item_id in user_carts[user_id]:
        user_carts[user_id][item_id] += qty
    else:
        user_carts[user_id][item_id] = qty

    total_items = sum(user_carts[user_id].values())
    await call.answer(
        f"✅ {item['name']} savatga qo'shildi!\nSavatda jami: {total_items} ta mahsulot",
        show_alert=True
    )


@router.callback_query(F.data.startswith("back_cat:"))
async def back_to_category(call: CallbackQuery):
    item_id = call.data.split(":")[1]
    # Kategoriyani topish
    for cat_key, cat_data in MENU.items():
        for item in cat_data["items"]:
            if item["id"] == item_id:
                await call.message.edit_text(
                    f"{cat_data['name']}\n\nQuyidagilardan birini tanlang:",
                    reply_markup=category_items_kb(cat_key)
                )
                return


# ─── SAVATCHA ────────────────────────────────────────────────────────────────────

@router.message(F.text == "🛒 Savatcha")
async def show_cart(message: Message):
    user_id = message.from_user.id
    cart = user_carts.get(user_id, {})

    if not cart:
        await message.answer(
            "🛒 Savatchingiz bo'sh!\n\nMenyudan taom tanlang 👇",
            reply_markup=main_menu_kb()
        )
        return

    text, total = build_cart_text(cart)
    await message.answer(
        f"🛒 <b>Sizning savatchingiz:</b>\n\n{text}\n"
        f"💳 <b>Jami: {total:,} so'm</b>\n\n"
        f"Buyurtmani rasmiylashtirasizmi?",
        parse_mode="HTML",
        reply_markup=cart_kb()
    )


def build_cart_text(cart: dict) -> tuple[str, int]:
    text = ""
    total = 0
    for i, (item_id, qty) in enumerate(cart.items(), 1):
        item = get_item_by_id(item_id)
        if item:
            subtotal = item["price"] * qty
            total += subtotal
            text += f"{i}. {item['emoji']} {item['name']}\n"
            text += f"   {qty} × {item['price']:,} = <b>{subtotal:,} so'm</b>\n\n"
    return text, total


@router.callback_query(F.data == "clear_cart")
async def clear_cart(call: CallbackQuery):
    user_carts[call.from_user.id] = {}
    await call.message.edit_text(
        "🗑️ Savat tozalandi. Qaytadan buyurtma bering 👇"
    )


# ─── CHECKOUT ────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "checkout")
async def checkout(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    cart = user_carts.get(user_id, {})

    if not cart:
        await call.answer("Savatcha bo'sh!", show_alert=True)
        return

    await state.set_state(OrderStates.waiting_contact)
    await call.message.answer(
        "📱 <b>Telefon raqamingizni ulashing</b>\n\n"
        "Buyurtmani tasdiqlash va yetkazib berish uchun haqiqiy raqamingiz kerak.\n\n"
        "⚠️ <i>Yolg'on raqam berilsa, buyurtma bekor qilinadi.</i>\n\n"
        "Quyidagi tugmani bosing 👇",
        parse_mode="HTML",
        reply_markup=share_contact_kb()
    )


@router.message(OrderStates.waiting_contact, F.contact)
async def receive_contact(message: Message, state: FSMContext):
    contact: Contact = message.contact
    user_id = message.from_user.id

    # Telefon raqam haqiqiyligini tekshirish (faqat o'z raqami)
    if contact.user_id != user_id:
        await message.answer(
            "❌ Iltimos, faqat o'z telefon raqamingizni ulashing!",
            reply_markup=share_contact_kb()
        )
        return

    user_contacts[user_id] = contact.phone_number
    await state.update_data(phone=contact.phone_number)
    await state.set_state(OrderStates.waiting_location)

    await message.answer(
        "✅ Telefon raqam qabul qilindi!\n\n"
        "📍 <b>Endi lokatsiyangizni ulashing</b>\n\n"
        "Yetkazib berish manzilini aniq belgilang.\n\n"
        "⚠️ <i>Yolg'on lokatsiya kiritish taqiqlangan!</i>\n\n"
        "👇 Quyidagi tugmani bosing:",
        parse_mode="HTML",
        reply_markup=share_location_kb()
    )


@router.message(OrderStates.waiting_contact)
async def wrong_contact(message: Message):
    await message.answer(
        "⚠️ Iltimos, quyidagi tugmani bosib telefon raqamingizni ulashing:",
        reply_markup=share_contact_kb()
    )


@router.message(OrderStates.waiting_location, F.location)
async def receive_location(message: Message, state: FSMContext, bot: Bot):
    location: Location = message.location

    # Live location tekshirish (yolg'on lokatsiyaning oldini olish)
    if message.location.live_period:
        await message.answer(
            "⚠️ Iltimos, 'Live location' emas, oddiy lokatsiyangizni yuboring.",
            reply_markup=share_location_kb()
        )
        return

    await state.update_data(
        lat=location.latitude,
        lon=location.longitude
    )

    data = await state.get_data()
    user_id = message.from_user.id
    cart = user_carts.get(user_id, {})
    cart_text, total = build_cart_text(cart)

    maps_link = f"https://maps.google.com/?q={location.latitude},{location.longitude}"

    confirm_text = (
        f"📋 <b>Buyurtmangizni tasdiqlang:</b>\n\n"
        f"{cart_text}"
        f"💳 <b>Jami: {total:,} so'm</b>\n\n"
        f"📱 Telefon: <code>{data['phone']}</code>\n"
        f"📍 <a href='{maps_link}'>Manzilni xaritada ko'rish</a>\n\n"
        f"✅ Buyurtmani tasdiqlaysizmi?"
    )

    await state.set_state(OrderStates.confirming_order)
    await message.answer(
        confirm_text,
        parse_mode="HTML",
        reply_markup=checkout_confirm_kb(),
        disable_web_page_preview=True
    )


@router.message(OrderStates.waiting_location)
async def wrong_location(message: Message):
    await message.answer(
        "⚠️ Iltimos, quyidagi tugmani bosib lokatsiyangizni ulashing:",
        reply_markup=share_location_kb()
    )


@router.callback_query(F.data == "confirm_order", OrderStates.confirming_order)
async def confirm_order(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = call.from_user.id
    data = await state.get_data()
    cart = user_carts.get(user_id, {})

    if not cart:
        await call.answer("Savatcha bo'sh!", show_alert=True)
        return

    order_id = str(uuid.uuid4())[:8].upper()
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    cart_text, total = build_cart_text(cart)
    maps_link = f"https://maps.google.com/?q={data['lat']},{data['lon']}"

    # Xaridorga xabar
    await call.message.edit_text(
        f"🎉 <b>Xaridingiz uchun rahmat!</b>\n\n"
        f"Buyurtmangiz kafe ma'muriyatiga yetkazildi.\n\n"
        f"📦 Buyurtma raqami: <code>#{order_id}</code>\n"
        f"⏰ Vaqt: {now}\n\n"
        f"Buyurtmangiz holati haqida sizga xabar berib boramiz! 🚀",
        parse_mode="HTML",
        reply_markup=None
    )
    await call.message.answer(
        "🏠 Asosiy menyuga qaytish:",
        reply_markup=main_menu_kb()
    )

    # Admin uchun xabar
    user = call.from_user
    username = f"@{user.username}" if user.username else "Yo'q"

    admin_text = (
        f"🔔 <b>YANGI BUYURTMA!</b> #{order_id}\n"
        f"{'─' * 30}\n"
        f"👤 <b>Mijoz:</b> {user.first_name} {user.last_name or ''}\n"
        f"🆔 <b>Telegram ID:</b> <code>{user_id}</code>\n"
        f"📱 <b>Telefon:</b> <code>{data['phone']}</code>\n"
        f"🔗 <b>Username:</b> {username}\n"
        f"⏰ <b>Vaqt:</b> {now}\n"
        f"{'─' * 30}\n"
        f"🛒 <b>Buyurtma:</b>\n{cart_text}"
        f"💳 <b>JAMI: {total:,} so'm</b>\n"
        f"{'─' * 30}\n"
        f"📍 <a href='{maps_link}'>Xaritada manzilni ko'rish</a>"
    )

    admin_msg = await bot.send_message(
        ADMIN_ID,
        admin_text,
        parse_mode="HTML",
        reply_markup=admin_order_kb(f"{order_id}:{user_id}"),
        disable_web_page_preview=False
    )

    # Buyurtma ma'lumotlarini saqlash
    user_orders[order_id] = {
        "user_id": user_id,
        "cart": dict(cart),
        "total": total,
        "phone": data["phone"],
        "lat": data["lat"],
        "lon": data["lon"],
        "time": now,
        "status": "new"
    }
    order_msg_ids[order_id] = (ADMIN_ID, admin_msg.message_id)

    # Savatni tozalash
    user_carts[user_id] = {}
    await state.clear()


@router.callback_query(F.data == "edit_order")
async def edit_order(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("✏️ Savatga qaytdingiz. O'zgartirishlar kiriting.")
    await call.message.answer("🛒 Savatingizni yangilang:", reply_markup=main_menu_kb())


@router.callback_query(F.data == "cancel_order")
async def cancel_order_user(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_carts[call.from_user.id] = {}
    await call.message.edit_text("❌ Buyurtma bekor qilindi.")
    await call.message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_kb())


# ─── ADMIN BUYURTMA HOLATI ────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("admin:"))
async def admin_update_status(call: CallbackQuery, bot: Bot):
    # Faqat admin uchun
    if call.from_user.id != ADMIN_ID:
        await call.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    parts = call.data.split(":")
    action = parts[1]
    order_id = parts[2]
    user_id_str = parts[3] if len(parts) > 3 else None

    order = user_orders.get(order_id)
    if not order:
        await call.answer("Buyurtma topilmadi", show_alert=True)
        return

    status_map = {
        "cooking": ("👨‍🍳 Tayyorlashga kirishildi", "🍳 Buyurtmangiz tayyorlanmoqda! Kuting..."),
        "delivered": ("🛵 Kuryerga berildi", "🛵 Buyurtmangiz yo'lda! Tez orada yetib keladi."),
        "done": ("✅ Yakunlandi", "✅ Buyurtmangiz yetkazildi! Ishtaha bo'lsin! 😊"),
        "cancel": ("❌ Bekor qilindi", "❌ Afsuski, buyurtmangiz bekor qilindi. Kechirasiz."),
    }

    admin_status, user_msg = status_map.get(action, ("Noma'lum", ""))

    # Admin xabarini yangilash
    order_info = order_msg_ids.get(order_id)
    if order_info:
        try:
            current_text = call.message.text or call.message.caption or ""
            new_text = current_text + f"\n\n🔄 <b>Holat: {admin_status}</b>"
            await bot.edit_message_text(
                new_text,
                chat_id=order_info[0],
                message_id=order_info[1],
                parse_mode="HTML",
                reply_markup=None if action in ["done", "cancel"] else admin_order_kb(f"{order_id}:{order['user_id']}")
            )
        except Exception:
            pass

    # Xaridorga xabar
    user_id = order.get("user_id")
    if user_id and user_msg:
        try:
            await bot.send_message(
                user_id,
                f"📦 <b>Buyurtma #{order_id} holati yangilandi</b>\n\n{user_msg}",
                parse_mode="HTML"
            )
        except Exception:
            pass

    user_orders[order_id]["status"] = action
    await call.answer(f"✅ {admin_status}", show_alert=True)


# ─── QO'LLAB-QUVVATLASH ──────────────────────────────────────────────────────────

@router.message(F.text == "📞 Qo'llab-quvvatlash")
async def support(message: Message):
    await message.answer(
        "📞 <b>Qo'llab-quvvatlash</b>\n\n"
        "Savol yoki muammo bo'lsa:\n\n"
        "👨‍💼 Admin: @adminusername\n"
        "📱 Telefon: +998 XX XXX XX XX\n"
        "⏰ Ish vaqti: 09:00 - 22:00\n\n"
        "Tez orada javob beramiz! 😊",
        parse_mode="HTML"
    )


# ─── ADMIN KOMANDALAR ─────────────────────────────────────────────────────────────

@router.message(Command("orders"))
async def list_orders(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    if not user_orders:
        await message.answer("📭 Hozircha buyurtmalar yo'q.")
        return

    text = "📊 <b>Barcha buyurtmalar:</b>\n\n"
    for oid, order in list(user_orders.items())[-10:]:
        text += f"#{oid} — {order['total']:,} so'm — {order['status']} — {order['time']}\n"

    await message.answer(text, parse_mode="HTML")


@router.message(Command("stats"))
async def stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    total_orders = len(user_orders)
    total_revenue = sum(o["total"] for o in user_orders.values())
    active = sum(1 for o in user_orders.values() if o["status"] not in ["done", "cancel"])

    await message.answer(
        f"📈 <b>Statistika:</b>\n\n"
        f"📦 Jami buyurtmalar: <b>{total_orders}</b>\n"
        f"✅ Faol buyurtmalar: <b>{active}</b>\n"
        f"💰 Jami daromad: <b>{total_revenue:,} so'm</b>",
        parse_mode="HTML"
    )
