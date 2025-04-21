"""
Bot command and message handlers for the Telegram question checker bot.

This file contains all the handler functions that process different types of
user interactions with the Telegram bot, including command handlers, message handlers,
and callback query handlers.
"""

import os
import tempfile
import logging
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.core.parser import parse_text_file
from src.core.formatters import (
    transform_to_student_format,
    transform_to_program_format,
    create_student_format_word,
    create_program_format_word,
    create_word_document,
    create_duplicate_report_word,
)
from src.core.duplicate_checker import generate_duplicate_report
from src.bot.messages import (
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    FILE_RECEIVED_MESSAGE,
    DUPLICATE_REPORT_MESSAGE,
    NO_DUPLICATES_MESSAGE,
    FORMAT_CHOICE_MESSAGE,
    INVALID_FILE_MESSAGE,
    GENERATING_FORMAT_MESSAGE,
    COMPLETED_MESSAGE,
)

# Define user states for conversation handling
WAITING_FOR_FILE, WAITING_FOR_FORMAT_CHOICE = range(2)
user_states = {}
user_data = {}

# Configure logging
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command to begin bot interaction.
    
    Sends welcome message, example file, and resets user state to waiting for file upload.
    """
    # Send welcome message
    await update.message.reply_text(WELCOME_MESSAGE)
    
    # Reset user state
    user_id = update.effective_user.id
    user_states[user_id] = WAITING_FOR_FILE
    if user_id in user_data:
        user_data.pop(user_id, None)
    
    # Send example file
    await update.message.reply_text("Savollar quyidagi formatda bo'lishi kerak. Namuna fayl:")
    
    # Get the path to the example file
    example_file_path = os.path.join(os.path.dirname(__file__), "namuna.txt")
    
    # Send the example file
    await context.bot.send_document(
        chat_id=user_id,
        document=open(example_file_path, 'rb'),
        filename="namuna.txt"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command to provide usage instructions.
    
    Sends detailed help message with formatting examples.
    """
    await update.message.reply_text(HELP_MESSAGE, parse_mode='Markdown')


async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Process uploaded document files from users.
    
    Validates file format, parses questions, checks for duplicates,
    and prompts user for format selection.
    """
    user_id = update.effective_user.id
    
    if user_id not in user_states or user_states[user_id] != WAITING_FOR_FILE:
        await update.message.reply_text(WELCOME_MESSAGE)
        user_states[user_id] = WAITING_FOR_FILE
        return
    
    if not update.message.document:
        await update.message.reply_text("Iltimos, .txt formatidagi fayl yuboring.")
        return
        
    file = update.message.document
    file_name = file.file_name
    
    # Check file extension
    if not file_name.lower().endswith('.txt'):
        await update.message.reply_text(INVALID_FILE_MESSAGE)
        return
    
    await update.message.reply_text(FILE_RECEIVED_MESSAGE)
    
    # Download and process the file
    await _process_uploaded_file(update, context, file, file_name, user_id)


async def _process_uploaded_file(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                file: Any, file_name: str, user_id: int) -> None:
    """
    Download and process the uploaded file.
    
    Handles file download, parsing, and duplicate checking.
    """
    # Download the file
    new_file = await context.bot.get_file(file.file_id)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        file_path = temp_file.name
    
    # Save file content to temp file
    await new_file.download_to_drive(file_path)
    
    try:
        # Parse the file
        json_data = parse_text_file(file_path)
        
        # Store data for this user
        user_data[user_id] = {
            'json_data': json_data,
            'file_path': file_path,
            'file_name': os.path.splitext(file_name)[0]
        }
        
        # Process duplicates and show format selection
        await _check_duplicates_and_prompt_format(update, context, json_data, user_id)
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        await update.message.reply_text(f"❌ Xato! Faylni qayta ishlashda muammo yuzaga keldi: {str(e)}")
        if os.path.exists(file_path):
            os.unlink(file_path)


async def _check_duplicates_and_prompt_format(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                             json_data: Dict, user_id: int) -> None:
    """
    Check for duplicate questions and prompt user for format selection only if no duplicates found.
    
    Checks for:
    1. Identical questions
    2. Identical answer variants across different questions
    3. Identical options within the same question
    
    If any duplicates are found, stops the workflow and sends a report.
    """
    # Check for duplicates
    duplicate_report = generate_duplicate_report(json_data)
    
    if "No duplicate or similar content found" in duplicate_report:
        await update.message.reply_text(NO_DUPLICATES_MESSAGE)
        # Show format selection buttons since no duplicates were found
        await _show_format_selection(update, context, user_id)
    else:
        # Send duplicate report message
        await update.message.reply_text(DUPLICATE_REPORT_MESSAGE)
        
        # Generate Word document for duplicate report
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as report_file:
            report_path = report_file.name
        
        # Create report Word document
        create_duplicate_report_word(duplicate_report, report_path)
        
        # Send duplicate report as a Word document
        await context.bot.send_document(
            chat_id=user_id, 
            document=open(report_path, 'rb'),
            filename=f"{user_data[user_id]['file_name']}_takrorlanishlar.docx"
        )
        os.unlink(report_path)
        
        # Clear user state and inform that they need to fix duplicates before proceeding
        user_states[user_id] = WAITING_FOR_FILE
        await update.message.reply_text(
            "❌ Savollaringizda takrorlanishlar mavjud. Iltimos, avval takrorlanishlarni bartaraf qiling, "
            "so'ng faylni qayta yuboring. Konvertatsiya jarayoni to'xtatildi."
        )
        
        # Clean up the uploaded file
        if 'file_path' in user_data[user_id] and os.path.exists(user_data[user_id]['file_path']):
            os.unlink(user_data[user_id]['file_path'])
        user_data.pop(user_id, None)

async def _show_format_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """
    Display format selection buttons to the user.
    
    Creates inline keyboard with format options and updates user state.
    """
    # Create keyboard for format selection
    keyboard = [
        [
            InlineKeyboardButton("Talaba formati", callback_data="student"),
            InlineKeyboardButton("Variantsiz talaba formati", callback_data="student_novariant")
        ],
        [
            InlineKeyboardButton("HEMIS formati", callback_data="program"),
            InlineKeyboardButton("Jadval (Word) formati", callback_data="word")
        ],
        [
            InlineKeyboardButton("Barcha formatlar", callback_data="all")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Ask user to select format
    await update.message.reply_text(FORMAT_CHOICE_MESSAGE, reply_markup=reply_markup)
    user_states[user_id] = WAITING_FOR_FORMAT_CHOICE


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle button callback queries for format selection.
    
    Generates and sends requested format(s) based on user selection.
    """
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if user_id not in user_states or user_states[user_id] != WAITING_FOR_FORMAT_CHOICE:
        await query.edit_message_text(text="⚠️ Sessiya vaqti tugadi. Iltimos, /start ni bosib qaytadan boshlang.")
        return
    
    selected_format = query.data
    
    if user_id not in user_data:
        await context.bot.send_message(
            chat_id=user_id, 
            text="⚠️ Sessiya ma'lumotlari yo'qoldi. Iltimos, /start ni bosib qaytadan boshlang."
        )
        return
    
    await query.edit_message_text(text=GENERATING_FORMAT_MESSAGE.format(selected_format))
    await _generate_selected_formats(context, user_id, selected_format)


async def _generate_selected_formats(context: ContextTypes.DEFAULT_TYPE, 
                                   user_id: int, selected_format: str) -> None:
    """
    Generate and send files in the selected format(s).
    
    Creates temporary files in the requested formats and sends them to the user.
    """
    json_data = user_data[user_id]['json_data']
    file_name = user_data[user_id]['file_name']
    
    # Create a temporary directory to store output files
    with tempfile.TemporaryDirectory() as temp_dir:
        formats_to_generate = ["student", "student_novariant", "program", "word"] if selected_format == "all" else [selected_format]
        
        for format_type in formats_to_generate:
            if format_type == "student":
                await _generate_student_format(context, user_id, json_data, file_name, temp_dir)
            elif format_type == "student_novariant":
                await _generate_student_novariant_format(context, user_id, json_data, file_name, temp_dir)
            elif format_type == "program":
                await _generate_hemis_format(context, user_id, json_data, file_name, temp_dir)
            elif format_type == "word":
                await _generate_word_table_format(context, user_id, json_data, file_name, temp_dir)
    
    # Send completion message with command buttons
    await context.bot.send_message(chat_id=user_id, text=COMPLETED_MESSAGE)
    
    # Clean up
    if 'file_path' in user_data[user_id] and os.path.exists(user_data[user_id]['file_path']):
        os.unlink(user_data[user_id]['file_path'])
    user_states[user_id] = WAITING_FOR_FILE


async def _generate_student_format(context: ContextTypes.DEFAULT_TYPE, user_id: int, 
                                 json_data: Dict, file_name: str, temp_dir: str) -> None:
    """
    Generate and send student format with variants.
    
    Creates a Word document with questions and answer variants.
    """
    output_path = os.path.join(temp_dir, f"{file_name}_TalabaVariant.docx")
    create_student_format_word(json_data, output_path, include_variants=True)
    
    await context.bot.send_document(
        chat_id=user_id,
        document=open(output_path, 'rb'),
        filename=f"{file_name}_TalabaVariant.docx"
    )


async def _generate_student_novariant_format(context: ContextTypes.DEFAULT_TYPE, user_id: int, 
                                           json_data: Dict, file_name: str, temp_dir: str) -> None:
    """
    Generate and send student format without variants.
    
    Creates a Word document with only questions, no answer variants.
    """
    output_path = os.path.join(temp_dir, f"{file_name}_TalabaNovariant.docx")
    create_student_format_word(json_data, output_path, include_variants=False)
    
    await context.bot.send_document(
        chat_id=user_id,
        document=open(output_path, 'rb'),
        filename=f"{file_name}_TalabaNovariant.docx"
    )


async def _generate_hemis_format(context: ContextTypes.DEFAULT_TYPE, user_id: int, 
                               json_data: Dict, file_name: str, temp_dir: str) -> None:
    """
    Generate and send HEMIS format as TXT file.
    
    Creates a text file with questions in HEMIS format.
    """
    output_path = os.path.join(temp_dir, f"{file_name}_Hemis.txt")
    hemis_text = transform_to_program_format(json_data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(hemis_text)
    
    await context.bot.send_document(
        chat_id=user_id,
        document=open(output_path, 'rb'),
        filename=f"{file_name}_Hemis.txt"
    )


async def _generate_word_table_format(context: ContextTypes.DEFAULT_TYPE, user_id: int, 
                                    json_data: Dict, file_name: str, temp_dir: str) -> None:
    """
    Generate and send Word document with questions in table format.
    
    Creates a Word document with tables for each question.
    """
    output_path = os.path.join(temp_dir, f"{file_name}_Yakuniy.docx")
    create_word_document(json_data, output_path)
    
    await context.bot.send_document(
        chat_id=user_id,
        document=open(output_path, 'rb'),
        filename=f"{file_name}_Yakuniy.docx"
    )


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle regular text messages from users.
    
    Provides guidance on file upload and available commands.
    """
    if update.message.text.startswith('/'):
        return
    
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