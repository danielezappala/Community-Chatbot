"""
Modulo per la gestione del comando /spesa del bot Telegram.

Questo modulo si occupa di processare il comando /spesa, validare i dati inseriti
dall'utente e salvare le spese su Google Sheets.
"""
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from typing import Tuple, Optional

from utils.validators import ExpenseValidator
from services.sheets import SheetsService
import logging

# Configurazione del logger per questo modulo
logger = logging.getLogger(__name__)

# Costanti per i messaggi di risposta
USAGE_MESSAGE = "Per aggiungere una spesa usa: /spesa <categoria> <importo> [descrizione]"
SUCCESS_MESSAGE = "✅ Spesa aggiunta con successo!"
ERROR_MESSAGE = "❌ Errore durante il salvataggio"

# Formato della data per il salvataggio su Google Sheets
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

async def handle_spesa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Gestisce il comando /spesa per l'aggiunta di una nuova spesa.
    
    Args:
        update: Oggetto Update di python-telegram-bot contenente il messaggio
        context: Oggetto Context di python-telegram-bot
        
    Il comando accetta i seguenti parametri:
    - categoria: Nome della categoria di spesa (es. 'cibo', 'trasporti')
    - importo: Valore numerico della spesa (può usare la virgola come decimale)
    - descrizione: Testo opzionale per descrivere la spesa
    """
    # Verifica che siano stati forniti i parametri minimi richiesti
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(USAGE_MESSAGE)
        return

    # Estrazione e pulizia dei parametri
    category = context.args[0].strip()
    amount_str = context.args[1].strip()
    description = " ".join(context.args[2:]).strip() if len(context.args) > 2 else "-"

    # Validazione della categoria
    is_valid, msg = ExpenseValidator.validate_category(category)
    if not is_valid:
        await update.message.reply_text(msg)
        return

    # Validazione dell'importo
    is_valid, msg, amount = ExpenseValidator.validate_amount(amount_str)
    if not is_valid:
        await update.message.reply_text(msg)
        return

    try:
        # Preparazione dati per il salvataggio
        expense_data = [
            datetime.now().strftime(DATE_FORMAT),  # Data e ora
            update.effective_user.username or "Anonimo",  # Utente
            category,  # Categoria
            str(amount),  # Importo
            description  # Descrizione
        ]
        
        # Salvataggio su Google Sheets
        sheets = SheetsService()
        success = sheets.add_expense(expense_data)

        # Invio del feedback all'utente
        await update.message.reply_text(SUCCESS_MESSAGE if success else ERROR_MESSAGE)
        
    except Exception as e:
        logger.error(f"Errore durante il salvataggio della spesa: {e}", exc_info=True)
        await update.message.reply_text("❌ Si è verificato un errore imprevisto")
