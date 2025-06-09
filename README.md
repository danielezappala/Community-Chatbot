# Community-Chatbot
Creare un chatbot Telegram con funzionalità base e avanzate per unire l'esperienza dei senior con la freschezza dei junior.
Il chatbot avrà una gestione delle spese che salverà su un foglio google (google sheets), da cui potrà analizzare i dati, magari divisi per categorie e commentati.
Oltre alla gestione spese avrà anche una gestione del calendario, dove l'utente potrà chiedere in linguaggio naturale al chatbot di inserire, modificare o cancellare eventi di google calendar.
Per beginner:
- creazione chatbot telegram
- collegamento di un foglio google tramite API
- scrittura e lettura foglio google
- strutturazione chatbot con comandi custom
Per esperti:
- utilizzo del chatbot sopra citato
- applicazione agentica con llm per gestire i calendari google
Le funzionalità e le modalità sono a discrezione della community. Potranno essere aggiunte funzionalità, grafiche, analisi, e così via.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd community-chatbot
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your Telegram Bot Token:**
    - Get your Bot Token from BotFather on Telegram.
    - You will need to set this token as an environment variable or directly in the `bot.py` script (though using an environment variable is recommended for security). For now, the `bot.py` script has a placeholder `YOUR_TELEGRAM_BOT_TOKEN`. You should replace this placeholder with your actual token.
    *Important Note for contributors:* Do not commit your actual bot token to the repository.
5.  **Run the bot:**
    ```bash
    python bot.py
    ```
