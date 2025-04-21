"""
Bot message templates for the Telegram question checker bot.

This file contains all the text messages used in the bot's interactions with users,
including welcome messages, help text, status updates, and error notifications.
All messages are in Uzbek language.
"""

# Welcome and help messages
WELCOME_MESSAGE = """
👋 Assalomu alaykum! Men test savollari tekshiruvchisi va formatlash botiman.

Men quyidagi imkoniyatlarga egaman:
- Test savollaridagi takrorlanishlarni tekshirish
- Savollarni turli formatlarga o'zgartirish

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
2. Takrorlanayotgan savollarning hisobotini olasiz
3. Kerakli format(lar)ni tanlang

Savollar formati quyidagicha bo'lishi kerak:

1. Savol matni?
a) Javob varianti 1
b) *To'g'ri javob varianti
c) Javob varianti 3
d) Javob varianti 4
To'g'ri javob oldiga * belgisini qo'ying.
"""

# File processing messages
FILE_RECEIVED_MESSAGE = "✅ Fayl qabul qilindi! Tekshirilmoqda..."
INVALID_FILE_MESSAGE = "❌ Xato! Faylning formati noto'g'ri. Iltimos, .txt faylini yuboring."

DUPLICATE_REPORT_MESSAGE = "⚠️ Quyidagi xatolar aniqlandi: (1) Bir xil savollar yoki (2) Bir savol ichida bir xil variantlar! Quyidagi hisobotda batafsil ma'lumot berilgan:"
NO_DUPLICATES_MESSAGE = "✅ Takrorlanishlar topilmadi! Barcha savollar noyob va har bir savol ichidagi variantlar ham noyob."
DUPLICATES_FOUND_ERROR = "❌ Savollaringizda xatoliklar mavjud: takrorlanayotgan savollar yoki bir savol ichida bir xil variantlar. Iltimos, avval xatolarni bartaraf qiling, so'ng faylni qayta yuboring. Konvertatsiya jarayoni to'xtatildi."

# Format selection and generation messages
FORMAT_CHOICE_MESSAGE = "Qaysi formatga aylantirmoqchi ekanligingizni tanlang:"
GENERATING_FORMAT_MESSAGE = "⏳ {} formatida tayyorlanmoqda..."
COMPLETED_MESSAGE = """
✅ Tayyor! Natijalarni yuklab oling.
"""

# Error messages
SESSION_TIMEOUT_MESSAGE = "⚠️ Sessiya vaqti tugadi. Iltimos, /start ni bosib qaytadan boshlang."
SESSION_DATA_LOST_MESSAGE = "⚠️ Sessiya ma'lumotlari yo'qoldi. Iltimos, /start ni bosib qaytadan boshlang."
PROCESSING_ERROR_MESSAGE = "❌ Xato! Faylni qayta ishlashda muammo yuzaga keldi: {}"

# Text message response
TEXT_MESSAGE_RESPONSE = """
Iltimos, .txt formatidagi fayl yuboring. Fayl quyidagi formatda bo'lishi kerak:

1. Savol matni?
a) Javob varianti 1
b) *To'g'ri javob varianti
c) Javob varianti 3
"""