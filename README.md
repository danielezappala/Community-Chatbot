# Community-Chatbot
Creare un chatbot Telegram con funzionalità base e avanzate per unire l'esperienza dei senior con la freschezza dei junior.
Il chatbot avrà una gestione delle spese che salverà su un foglio google (google sheets), da cui potrà analizzare i dati, magari divisi per categorie e commentati.
Oltre alla gestione spese avrà anche una gestione del calendario, dove l'utente potrà chiedere in linguaggio naturale al chatbot di inserire, modificare o cancellare eventi di google calendar.

## Features
- **Telegram Bot Interface:** Basic command handling.
- **Expense Tracking:** Add expenses to a Google Sheet via a bot command.

## Project Goals
**For Beginners:**
- Creazione chatbot Telegram.
- Collegamento di un foglio Google tramite API.
- Scrittura e lettura foglio Google.
- Strutturazione chatbot con comandi custom.
**For Experts:**
- Utilizzo del chatbot sopra citato.
- Applicazione agentica con LLM per gestire i calendari Google.

Le funzionalità e le modalità sono a discrezione della community. Potranno essere aggiunte funzionalità, grafiche, analisi, e così via.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd community-chatbot
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install or Update Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If you have an existing installation, re-run this command to ensure all dependencies, including those for Google API access, are installed.*

4.  **Set up your Telegram Bot Token:**
    - Get your Bot Token from BotFather on Telegram.
    - In `bot.py`, replace the placeholder `"YOUR_TELEGRAM_BOT_TOKEN"` with your actual token.
    ```python
    # In bot.py
    TELEGRAM_BOT_TOKEN = "YOUR_ACTUAL_TELEGRAM_BOT_TOKEN"
    ```
    *Important Note for contributors:* Do not commit your actual bot token to the repository. Using environment variables for tokens is a best practice for deployed applications.

5.  **Set up Google Sheets Integration (for expense tracking):**
    See the "Google Sheets Integration Setup" section below.

6.  **Run the bot:**
    ```bash
    python bot.py
    ```

## Bot Commands

### `/start`
- **Purpose:** Initializes the bot and sends a welcome message.
- **Syntax:** `/start`

### `/addexpense`
- **Purpose:** Adds an expense entry to the connected Google Sheet.
- **Syntax:** `/addexpense <Category> <Amount> [Description...]`
    - `<Category>`: The category of the expense (e.g., Food, Transport, Utilities).
    - `<Amount>`: The numerical amount of the expense.
    - `[Description...]`: (Optional) A brief description of the expense.
- **Example:** `/addexpense Food 12.50 Lunch with colleagues`

## Google Sheets Integration Setup

The bot is configured to write expense data to a specific Google Sheet. To enable this functionality, follow these steps:

1.  **Google Cloud Project:**
    *   Create a new project in the [Google Cloud Console](https://console.cloud.google.com/) or use an existing one.
2.  **Enable Google Sheets API:**
    *   In your Google Cloud Project, navigate to "APIs & Services" > "Library".
    *   Search for "Google Sheets API" and enable it for your project.
3.  **Create Service Account:**
    *   Go to "APIs & Services" > "Credentials".
    *   Click "Create Credentials" > "Service account".
    *   Fill in the service account details (name, ID, description).
    *   Grant any necessary roles (though for simply writing to a sheet via its API, specific roles might not be strictly needed here if the sheet is shared directly, but "Project" > "Editor" can be a starting point if issues arise). Click "Done".
    *   Once created, find the service account in the list, click on it, go to the "Keys" tab.
    *   Click "Add Key" > "Create new key". Choose "JSON" as the key type and click "Create".
    *   A `credentials.json` file will be downloaded.
4.  **Place `credentials.json`:**
    *   Move the downloaded `credentials.json` file into the root directory of this project (the `community-chatbot` folder).
5.  **IMPORTANT: Add `credentials.json` to `.gitignore`:**
    *   To prevent your sensitive credentials from being committed to the repository, create or open the `.gitignore` file in the root of the project and add the following line:
        ```
        credentials.json
        ```
6.  **Share the Google Sheet:**
    *   Open the Google Sheet you want the bot to write to.
    *   Click the "Share" button (usually top right).
    *   In the "Add people and groups" field, paste the email address of the service account you created (you can find this in the service account details in the Google Cloud Console, it looks like `your-service-account-name@your-project-id.iam.gserviceaccount.com`).
    *   Ensure you give the service account "Editor" permissions for this sheet.
    *   Click "Send" or "Share".
7.  **Spreadsheet ID Configuration:**
    *   The bot currently uses a hardcoded `SPREADSHEET_ID` to identify the target Google Sheet. This is defined in `sheets_handler.py`:
        ```python
        # In sheets_handler.py
        SPREADSHEET_ID = '1lghaMKWcI9Fj_1mv9R2nTDp7S2Wxy1KPceCw8F7DgSM'
        ```
    *   If you are using your own Google Sheet, you will need to replace this ID with your sheet's ID. You can find your sheet's ID in its URL: `https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_IS_HERE/edit`.

By following these steps, the `/addexpense` command should be able to add entries to your designated Google Sheet.
