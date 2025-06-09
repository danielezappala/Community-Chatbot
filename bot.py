import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime
from sheets_handler import add_row_to_sheet

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Placeholder for the Telegram Bot Token
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the /start command is issued."""
    await update.message.reply_text("Hello! I am your community chatbot.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addexpense", add_expense_command))

    # log all errors
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

async def add_expense_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Adds an expense to the Google Sheet."""
    try:
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "Usage: /addexpense <Category> <Amount> [Description...]\n"
                "Example: /addexpense Food 15.50 Lunch with colleagues"
            )
            return

        category = context.args[0]
        amount_str = context.args[1]
        description_parts = context.args[2:]
        description = " ".join(description_parts) if description_parts else "-"

        # Basic validation for amount (can be improved)
        try:
            # Try to convert to float to ensure it's a number, but store as string
            # if your sheet expects strings for currency.
            # If your sheet expects numbers, store it as float.
            float(amount_str)
        except ValueError:
            await update.message.reply_text(
                "Invalid amount. Please provide a numeric value for the amount.\n"
                "Example: /addexpense Food 15.50 Lunch"
            )
            return

        current_date_str = datetime.now().strftime("%Y-%m-%d")

        # Values in the order: Date, Category, Amount, Description
        # Ensure this matches your Google Sheet column order
        values_to_add = [current_date_str, category, amount_str, description]

        logger.info(f"Attempting to add expense: {values_to_add}")

        if add_row_to_sheet(values_to_add):
            await update.message.reply_text("Spesa aggiunta con successo!")
            logger.info(f"Expense added successfully: {values_to_add}")
        else:
            await update.message.reply_text("Errore durante l'aggiunta della spesa al foglio Google.")
            logger.error(f"Failed to add expense after calling add_row_to_sheet: {values_to_add}")

    except Exception as e:
        logger.error(f"Error in add_expense_command: {e}", exc_info=True)
        await update.message.reply_text("An unexpected error occurred while adding the expense.")


if __name__ == "__main__":
    main()
