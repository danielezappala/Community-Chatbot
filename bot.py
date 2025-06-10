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
TELEGRAM_BOT_TOKEN = "8074566163:AAHrY-EO1pS2KfhnJSwVnuWtRHfdBs0g16s"

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
    
    # Set higher logging level for httpx to log all requests
    logging.getLogger("httpx").setLevel(logging.DEBUG)

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("spesa", spesa_command))
    application.add_handler(CommandHandler("addexpense", spesa_command))  # Add handler for addexpense
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("echo", echo))
    
    # Add a message handler to catch ALL messages for debugging
    application.add_handler(MessageHandler(filters.ALL, debug_message))

    # log all errors
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

async def spesa_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Adds an expense to the Google Sheet."""
    logger.info("spesa_command triggered")
    logger.info(f"Command arguments: {context.args}")
    try:
        if not context.args or len(context.args) < 2:
            await update.message.reply_text("Test spesa")
            return

        category = context.args[0]
        amount_str = context.args[1].replace(',', '.')  # Accetta sia virgola che punto
        description_parts = context.args[2:]
        description = " ".join(description_parts) if description_parts else "-"

        # Validazione importo
        try:
            float(amount_str)
        except ValueError:
            await update.message.reply_text(
                "L'importo deve essere un numero (es: 12.50 o 12,50)."
            )
            return

        # Prepara i dati da aggiungere allo sheet
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = update.effective_user.username or update.effective_user.first_name or "Anon"
        values_to_add = [now, user, category, amount_str, description]

        # Scrive sullo sheet e risponde SEMPRE
        if add_row_to_sheet(values_to_add):
            await update.message.reply_text("Spesa aggiunta con successo!")
            logger.info(f"Expense added successfully: {values_to_add}")
        else:
            await update.message.reply_text("Errore durante l'aggiunta della spesa al foglio Google. Controlla le credenziali, i permessi o il nome del foglio.")
            logger.error(f"Failed to add expense after calling add_row_to_sheet: {values_to_add}")

    except Exception as e:
        logger.error(f"Error in add_expense_command: {e}", exc_info=True)
        await update.message.reply_text("Si è verificato un errore inatteso durante l'aggiunta della spesa.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message: {update.message.text}")
    await update.message.reply_text("Echo: " + update.message.text)

async def debug_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Debug handler to log all incoming messages."""
    logger.info(f"DEBUG - Received message: {update.message.text}")
    if update.message.text and update.message.text.startswith(('/')):
        command_parts = update.message.text.split()
        command = command_parts[0][1:]  # Remove the slash
        logger.info(f"DEBUG - Detected command: {command} with args: {command_parts[1:]}")


if __name__ == "__main__":
    main()
