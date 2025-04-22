"""
Bot message templates for the Telegram question converter bot.

This file contains text messages used in the bot's interactions with users.
All messages are in Uzbek language.
"""

# Main messages
WELCOME_MESSAGE = """
👋 Assalomu alaykum! Men test savollari formatlash botiman.

Men quyidagi imkoniyatlarga egaman:
- Savollarni turli formatlarga o'zgartirish
- Test savollaridagi takrorlanishlarni tekshirish

Ishni boshlash uchun menga .txt formatidagi savollaringizni yuboring.

Savol formatining namunasi:
1. Savol matni?
a) Javob varianti 1
b) *To'g'ri javob varianti
c) Javob varianti 3
"""

HELP_MESSAGE = """
🔍 Botdan foydalanish yo'riqnomasi:

1. Menga .txt faylini yuboring (savollar va javoblar variantlari bilan)
2. Kerakli format(lar)ni tanlang

Savollar formati quyidagicha bo'lishi kerak:

1. Savol matni?
a) Javob varianti 1
b) *To'g'ri javob varianti
c) Javob varianti 3
d) Javob varianti 4

To'g'ri javob oldiga * belgisini qo'ying.
"""

# Status messages
FILE_RECEIVED_MESSAGE = "✅ Fayl qabul qilindi! Tekshirilmoqda..."
FORMAT_CHOICE_MESSAGE = "Qaysi formatga aylantirmoqchi ekanligingizni tanlang:"
GENERATING_FORMAT_MESSAGE = "⏳ {} formatida tayyorlanmoqda..."
COMPLETED_MESSAGE = "✅ Tayyor! Natijalarni yuklab oling."

# Error messages
INVALID_FILE_MESSAGE = (
    "❌ Xato! Faylning formati noto'g'ri. Iltimos, .txt faylini yuboring."
)
SESSION_TIMEOUT_MESSAGE = "⚠️ Sessiya vaqti tugadi. Iltimos, faylni qayta yuboring."
PROCESSING_ERROR_MESSAGE = "❌ Xato! Faylni qayta ishlashda muammo yuzaga keldi: {}"

# Duplicate checking messages
DUPLICATE_REPORT_MESSAGE = "⚠️ Quyidagi xatolar aniqlandi: (1) Bir xil savollar yoki (2) Bir savol ichida bir xil variantlar! Quyidagi hisobotda batafsil ma'lumot berilgan:"
NO_DUPLICATES_MESSAGE = (
    "✅ Takrorlanishlar topilmadi! Barcha savollar va variantlar noyob."
)
DUPLICATES_FOUND_ERROR = "❌ Savollaringizda xatoliklar mavjud: takrorlanayotgan savollar yoki bir savol ichida bir xil variantlar. Iltimos, avval xatolarni bartaraf qiling, so'ng faylni qayta yuboring."

# Text message response
TEXT_MESSAGE_RESPONSE = """
Iltimos, .txt formatidagi fayl yuboring. Fayl quyidagi formatda bo'lishi kerak:

1. Savol matni?
a) Javob varianti 1
b) *To'g'ri javob varianti
c) Javob varianti 3

Komandalar:
/help - Batafsil yo'riqnoma olish
/start - Botni qayta ishga tushirish
"""
