import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime
from src.services.sheets import SheetsService

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.DEBUG,  
    handlers=[
        logging.StreamHandler(),  
        logging.FileHandler('bot.log')  
    ]
)
logger = logging.getLogger(__name__)

# Placeholder for the Telegram Bot Token
TELEGRAM_BOT_TOKEN = "8074566163:AAHrY-EO1pS2KfhnJSwVnuWtRHfdBs0g16s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the /start command is issued."""
    print("INIZIO start command - PRINT")
    logger.info("INIZIO start command")
    await update.message.reply_text("Hello! I am your community chatbot.")
    logger.info("Risposta inviata: Hello message")
    print("Risposta inviata: Hello message - PRINT")

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
    application.add_handler(MessageHandler(~filters.COMMAND, debug_message))

    # log all errors
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

class ExpenseValidator:
    @staticmethod
    def validate_category(category: str) -> tuple[bool, str]:
        """Restituisce (success, error_message)"""
        cleaned = category.strip().replace('"','').replace("'",'').replace('“','').replace('”','')
        if not cleaned:
            return False, "❌ Categoria vuota o solo quote"
        return True, ""

    @staticmethod
    def validate_amount(amount_str: str) -> tuple[bool, str, float]:
        """Restituisce (success, error_message, cleaned_amount)"""
        try:
            amount = float(amount_str.replace(',','.'))
            if amount <= 0:
                return False, "❌ Importo deve essere positivo", 0
            return True, "", amount
        except ValueError:
            return False, "❌ Importo non numerico", 0

async def spesa_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Adds an expense to the Google Sheet."""
    print("INIZIO spesa_command - PRINT")
    logger.info("INIZIO spesa_command")
    print(f"Command arguments: {context.args}")
    logger.info(f"Command arguments: {context.args}")
    try:
        if not context.args or len(context.args) < 2:
            print("Ramo: args insufficienti - PRINT")
            await update.message.reply_text("Per aggiungere una spesa usa: /spesa <categoria> <importo> [descrizione]\nEsempio: /spesa cibo 12.50 pranzo")
            logger.info("Risposta inviata: istruzioni per uso comando spesa")
            print("Risposta inviata: istruzioni per uso comando spesa - PRINT")
            return

        category = context.args[0]
        amount_str = context.args[1]
        description_parts = context.args[2:]
        description = " ".join(description_parts) if description_parts else "-"

        print("Prima della validazione importo - PRINT")
        logger.info("Prima di preparare dati per Google Sheets")
        
        # Validazione categoria
        is_valid_category, error_message = ExpenseValidator.validate_category(category)
        if not is_valid_category:
            await update.message.reply_text(error_message)
            logger.warning(f"Validazione fallita - {error_message}. User: {update.effective_user.username}, Args: {context.args}")
            return

        # Validazione importo
        is_valid_amount, error_message, amount = ExpenseValidator.validate_amount(amount_str)
        if not is_valid_amount:
            await update.message.reply_text(error_message)
            logger.warning(f"Importo non valido ricevuto: {amount_str}")
            return

        # Validazione descrizione
        description = description.strip()
        if any(char in description for char in "#@!$%^&*()+=[]{};:'\"|<>?~`"):
            await update.message.reply_text("❌ Errore: La descrizione contiene caratteri speciali non permessi")
            logger.warning(f"Descrizione con caratteri speciali: {description}")
            return

        print("Prima della preparazione dati - PRINT")
        # Prepara i dati da aggiungere allo sheet
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = update.effective_user.username or update.effective_user.first_name or "Anon"
        values_to_add = [now, user, category, amount_str, description]

        print(f"Prima di chiamare add_row_to_sheet - PRINT. values_to_add: {values_to_add}")
        logger.info(f"Chiamo add_row_to_sheet con: {values_to_add}")
        sheets_service = SheetsService()
        result = sheets_service.add_expense(values_to_add)
        print(f"Dopo chiamata add_row_to_sheet - PRINT. result: {result}")
        logger.info(f"Risultato add_row_to_sheet: {result}")
        # Scrive sullo sheet e risponde SEMPRE
        if result:
            print("Ramo: Spesa aggiunta con successo - PRINT")
            await update.message.reply_text("Spesa aggiunta con successo!")
            logger.info("Risposta inviata: Spesa aggiunta con successo!")
            print("Risposta inviata: Spesa aggiunta con successo - PRINT")
            logger.info(f"Expense added successfully: {values_to_add}")
        else:
            print("Ramo: Errore durante l'aggiunta della spesa - PRINT")
            await update.message.reply_text("Errore durante l'aggiunta della spesa al foglio Google. Controlla le credenziali, i permessi o il nome del foglio.")
            logger.info("Risposta inviata: Errore durante l'aggiunta della spesa al foglio Google")
            print("Risposta inviata: Errore durante l'aggiunta della spesa - PRINT")
            logger.error(f"Failed to add expense after calling add_row_to_sheet: {values_to_add}")

    except Exception as e:
        print(f"Entrato nell'except di spesa_command - PRINT. Errore: {e}")
        logger.error(f"Error in add_expense_command: {e}", exc_info=True)
        logger.info("Entrato nell'except di spesa_command")
        await update.message.reply_text("Si è verificato un errore inatteso durante l'aggiunta della spesa.")
        print("Risposta inviata: Errore inatteso durante l'aggiunta della spesa - PRINT")
        logger.info("Risposta inviata: Errore inatteso durante l'aggiunta della spesa")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message: {update.message.text}")
    await update.message.reply_text("Echo: " + update.message.text)

async def debug_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ignora i comandi, lascia che li gestisca il CommandHandler
    if update.message.text and update.message.text.startswith('/'):
        return
    logger.info(f"DEBUG - Received message: {update.message.text}")

if __name__ == "__main__":
    main()
