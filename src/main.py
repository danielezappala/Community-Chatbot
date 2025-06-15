"""
Punto di ingresso principale del bot
"""
from telegram.ext import Application, CommandHandler
from handlers.expenses import handle_spesa
import logging

TELEGRAM_BOT_TOKEN = '8074566163:AAHrY-EO1pS2KfhnJSwVnuWtRHfdBs0g16s'

def main():
    # Configurazione logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Registrazione handlers
    application.add_handler(CommandHandler("spesa", handle_spesa))
    
    application.run_polling()

if __name__ == '__main__':
    main()
