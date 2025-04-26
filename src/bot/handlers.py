"""
Bot command and message handlers for the Telegram question converter bot.

This file contains handlers for processing user interactions with the bot,
including commands and file uploads.
"""

import os
import tempfile
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.core.parser import parse_text_file
from src.core.formatters import (
    transform_to_student_format,
    create_student_word_document,
    transform_to_program_format,
    create_word_document,
)
from src.core.duplicate_checker import check_for_duplicates


# Basic welcome message
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

# Help message
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


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command to begin bot interaction.
    """
    # Send welcome message
    await update.message.reply_text(WELCOME_MESSAGE)

    # Send example file
    example_file_path = os.path.join(os.path.dirname(__file__), "namuna.txt")
    if os.path.exists(example_file_path):
        await update.message.reply_text(
            "Savollar quyidagi formatda bo'lishi kerak. Namuna fayl:"
        )
        await context.bot.send_document(
            chat_id=update.effective_user.id,
            document=open(example_file_path, "rb"),
            filename="namuna.txt",
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command to provide usage instructions.
    """
    await update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")


async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Process uploaded document files from users.
    """
    if not update.message.document:
        await update.message.reply_text("Iltimos, .txt formatidagi fayl yuboring.")
        return

    file = update.message.document
    file_name = file.file_name

    # Check file extension
    if not file_name.lower().endswith(".txt"):
        await update.message.reply_text(
            "Iltimos, faqat .txt formatidagi fayllar qabul qilinadi."
        )
        return

    await update.message.reply_text("✅ Fayl qabul qilindi! Tekshirilmoqda...")

    # Download file to a temporary location
    new_file = await context.bot.get_file(file.file_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        file_path = temp_file.name

    await new_file.download_to_drive(file_path)

    try:
        # Parse the file
        json_data = parse_text_file(file_path)

        # Check for duplicates
        duplicate_report = check_for_duplicates(json_data)

        if "No duplicate" not in duplicate_report:
            # Send report if duplicates found
            await update.message.reply_text(
                "⚠️ Quyidagi xatolar aniqlandi:\n\n"
                + duplicate_report
                + "\n\nIltimos, avval takrorlanishlarni bartaraf qiling, so'ng faylni qayta yuboring."
            )
            os.unlink(file_path)  # Clean up the file
            return

        # Store data in user context
        context.user_data["json_data"] = json_data
        context.user_data["file_path"] = file_path
        context.user_data["file_name"] = os.path.splitext(file_name)[0]

        # Show format selection buttons
        await show_format_selection(update, context)

    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.unlink(file_path)
        await update.message.reply_text(
            f"❌ Xato! Faylni qayta ishlashda muammo yuzaga keldi: {str(e)}"
        )


async def show_format_selection(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Display format selection buttons to the user.
    """
    # Create keyboard for format selection
    keyboard = [
        [
            InlineKeyboardButton("Talaba formati", callback_data="student"),
            InlineKeyboardButton(
                "Variantsiz talaba formati", callback_data="student_novariant"
            ),
        ],
        [
            InlineKeyboardButton("HEMIS formati", callback_data="hemis"),
            InlineKeyboardButton("Jadval (Word) formati", callback_data="word"),
        ],
        [InlineKeyboardButton("Barcha formatlar", callback_data="all")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask user to select format
    await update.message.reply_text(
        "Qaysi formatga aylantirmoqchi ekanligingizni tanlang:",
        reply_markup=reply_markup,
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle format selection and generate appropriate files."""
    query = update.callback_query
    await query.answer()

    selected_format = query.data
    
    # Check for valid user data
    if not context.user_data.get("json_data"):
        await query.edit_message_text("⚠️ Sessiya vaqti tugadi. Iltimos, faylni qayta yuboring.")
        return

    await query.edit_message_text(f"⏳ {selected_format} formatida tayyorlanmoqda...")

    # Get stored data
    json_data = context.user_data["json_data"]
    file_name = context.user_data["file_name"]
    file_path = context.user_data["file_path"]

    # Determine formats to generate
    formats_to_generate = ["student", "student_novariant", "hemis", "word"] if selected_format == "all" else [selected_format]

    # Create temporary directory for output files
    with tempfile.TemporaryDirectory() as temp_dir:
        for format_type in formats_to_generate:
            try:
                if format_type == "hemis":
                    # HEMIS format (text file)
                    output_path = os.path.join(temp_dir, f"{file_name}_Hemis.txt")
                    hemis_text = transform_to_program_format(json_data)
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(hemis_text)
                    
                elif format_type == "student":
                    # Student format with variants (Word)
                    output_path = os.path.join(temp_dir, f"{file_name}_TalabaVariant.docx")
                    create_student_word_document(json_data, output_path, include_variants=True)
                    
                elif format_type == "student_novariant":
                    # Student format without variants (Word)
                    output_path = os.path.join(temp_dir, f"{file_name}_TalabaNovariant.docx")
                    create_student_word_document(json_data, output_path, include_variants=False)
                    
                elif format_type == "word":
                    # Word table format
                    output_path = os.path.join(temp_dir, f"{file_name}_Yakuniy.docx")
                    create_word_document(json_data, output_path)
                
                # Send file to user
                await context.bot.send_document(
                    chat_id=update.effective_user.id,
                    document=open(output_path, "rb"),
                    filename=os.path.basename(output_path)
                )
                
            except Exception as e:
                # logger.error(f"Error processing {format_type}: {str(e)}")
                await context.bot.send_message(
                    chat_id=update.effective_user.id,
                    text=f"❌ Xato! {format_type} formatini yaratishda muammo yuzaga keldi."
                )

    # Clean up
    if os.path.exists(file_path):
        os.unlink(file_path)
    context.user_data.clear()

    await context.bot.send_message(
        chat_id=update.effective_user.id, 
        text="✅ Tayyor! Natijalarni yuklab oling."
    )

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle regular text messages from users.
    """
    if update.message.text.startswith("/"):
        return  # Ignore commands

    await update.message.reply_text(
        "Iltimos, .txt formatidagi fayl yuboring. Fayl quyidagi formatda bo'lishi kerak:\n\n"
        "1. Savol matni?\n"
        "a) Javob varianti 1\n"
        "b) *To'g'ri javob varianti\n"
        "c) Javob varianti 3\n\n"
        "Komandalar:\n"
        "/help - Batafsil yo'riqnoma olish\n"
        "/start - Botni qayta ishga tushirish"
    )
