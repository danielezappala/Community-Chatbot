"""
Handler per il comando /spesa
"""
from telegram import Update
from telegram.ext import ContextTypes
from utils.validators import ExpenseValidator
from services.sheets import SheetsService
import logging

logger = logging.getLogger(__name__)

async def handle_spesa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler per il comando /spesa"""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Per aggiungere una spesa usa: /spesa <categoria> <importo> [descrizione]")
        return

    category = context.args[0]
    amount_str = context.args[1]
    description = " ".join(context.args[2:]) if len(context.args) > 2 else "-"

    # Validazione
    is_valid, msg = ExpenseValidator.validate_category(category)
    if not is_valid:
        await update.message.reply_text(msg)
        return

    is_valid, msg, amount = ExpenseValidator.validate_amount(amount_str)
    if not is_valid:
        await update.message.reply_text(msg)
        return

    # Aggiunta a Google Sheets
    sheets = SheetsService()
    success = sheets.add_expense([
        str(update.message.date),
        update.effective_user.username,
        category,
        str(amount),
        description
    ])

    if success:
        await update.message.reply_text("Spesa aggiunta con successo!")
    else:
        await update.message.reply_text("❌ Errore durante il salvataggio")
