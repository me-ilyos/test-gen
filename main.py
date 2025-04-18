"""
Entry point for the test question checker bot application.

This file contains the main function to initialize and run the Telegram bot,
setting up all the necessary handlers and configurations.
"""

import os
import logging
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
from src.utils.helpers import load_environment_variables


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def setup_handlers(application: Application) -> None:
    """
    Register all command and message handlers for the bot.
    
    Args:
        application: The Telegram bot application instance
    """
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.Document.ALL, receive_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    
    # Add callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))


def main() -> None:
    """
    Initialize and run the Telegram bot application.
    
    Loads environment variables, creates the bot application,
    sets up handlers, and starts the bot.
    """
    # Load environment variables
    env_vars = load_environment_variables()
    bot_token = env_vars.get("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        exit(1)
    
    # Create the application
    application = Application.builder().token(bot_token).build()
    
    # Setup handlers
    setup_handlers(application)
    
    # Log bot startup
    logger.info("Starting bot")
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()