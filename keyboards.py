from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from menu_data import MENU, get_item_by_id


def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🧊 Salqin Ichimliklar")
    builder.button(text="🍽️ Milliy Taomlar")
    builder.button(text="🍔 Fast Food")
    builder.button(text="🛒 Savatcha")
    builder.button(text="📞 Qo'llab-quvvatlash")
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def category_items_kb(category_key: str):
    items = MENU[category_key]["items"]
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(
            text=f"{item['emoji']} {item['name']} — {item['price']:,} so'm",
            callback_data=f"item:{item['id']}"
        )
    builder.button(text="🔙 Orqaga", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()


def item_detail_kb(item_id: str, qty: int = 1):
    builder = InlineKeyboardBuilder()
    builder.button(text="➖", callback_data=f"qty_minus:{item_id}:{qty}")
    builder.button(text=f"  {qty} ta  ", callback_data=f"qty_show:{item_id}:{qty}")
    builder.button(text="➕", callback_data=f"qty_plus:{item_id}:{qty}")
    builder.button(text="🛒 Savatga qo'shish", callback_data=f"add_cart:{item_id}:{qty}")
    builder.button(text="🔙 Orqaga", callback_data=f"back_cat:{item_id}")
    builder.adjust(3, 1, 1)
    return builder.as_markup()


def cart_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Buyurtmani rasmiylashtirish", callback_data="checkout")
    builder.button(text="🗑️ Savatni tozalash", callback_data="clear_cart")
    builder.button(text="🔙 Menyuga qaytish", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()


def checkout_confirm_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Tasdiqlash va yuborish", callback_data="confirm_order")
    builder.button(text="✏️ O'zgartirish", callback_data="edit_order")
    builder.button(text="❌ Bekor qilish", callback_data="cancel_order")
    builder.adjust(1)
    return builder.as_markup()


def share_contact_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📱 Telefon raqamimni ulashish", request_contact=True)
    builder.button(text="❌ Bekor qilish")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def share_location_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📍 Lokatsiyamni ulashish", request_location=True)
    builder.button(text="❌ Bekor qilish")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def admin_order_kb(order_id: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="👨‍🍳 Tayyorlashga kirishildi", callback_data=f"admin:cooking:{order_id}")
    builder.button(text="🛵 Kuryerga berildi", callback_data=f"admin:delivered:{order_id}")
    builder.button(text="✅ Yakunlandi", callback_data=f"admin:done:{order_id}")
    builder.button(text="❌ Bekor qilindi", callback_data=f"admin:cancel:{order_id}")
    builder.adjust(1)
    return builder.as_markup()


def channel_check_kb(channel_link: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Kanalga a'zo bo'lish", url=channel_link)
    builder.button(text="✅ A'zo bo'ldim", callback_data="check_subscription")
    builder.adjust(1)
    return builder.as_markup()
