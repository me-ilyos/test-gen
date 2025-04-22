"""
Entry point for the test question converter bot application.

This file initializes and runs the Telegram bot, setting up all the
necessary handlers and configurations.
"""

import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.bot.handlers import (
    start_command,
    help_command,
    receive_file,
    button_callback,
    text_message,
)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure basic logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", "bot.log")),
    ],
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Initialize and run the Telegram bot application.
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Load environment variables
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        logger.error("BOT_TOKEN environment variable not set")
        return

    # Create the application
    application = Application.builder().token(bot_token).build()

    # Setup handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, receive_file))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_message)
    )
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    logger.info("Starting Test Questions Converter Bot")
    application.run_polling()


if __name__ == "__main__":
    main()
