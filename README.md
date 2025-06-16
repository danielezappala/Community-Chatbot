# Community Chatbot per Gestione Spese

## README.md del branch main
Creare un chatbot Telegram con funzionalità base e avanzate per unire l'esperienza dei senior con la freschezza dei junior. Il chatbot avrà una gestione delle spese che salverà su un foglio google (google sheets), da cui potrà analizzare i dati, magari divisi per categorie e commentati. Oltre alla gestione spese avrà anche una gestione del calendario, dove l'utente potrà chiedere in linguaggio naturale al chatbot di inserire, modificare o cancellare eventi di google calendar. Per beginner:

creazione chatbot telegram
collegamento di un foglio google tramite API
scrittura e lettura foglio google
strutturazione chatbot con comandi custom Per esperti:
utilizzo del chatbot sopra citato
applicazione agentica con llm per gestire i calendari google Le funzionalità e le modalità sono a discrezione della community. Potranno essere aggiunte funzionalità, grafiche, analisi, e così via.


---

Un bot Telegram per la gestione delle spese condivise che salva i dati su Google Sheets. Il progetto è pensato per unire l'esperienza degli sviluppatori senior con la freschezza dei junior, creando uno strumento utile e ben strutturato.

## 🚀 Funzionalità

- **Gestione Spese**
  - Aggiungi spese con categoria, importo e descrizione
  - Salvataggio automatico su Google Sheets
  - Validazione degli input
  - Supporto a categorie personalizzate

- **Interfaccia Telegram**
  - Comandi intuitivi
  - Feedback immediato
  - Gestione degli errori

## 🎯 Obiettivi del Progetto

**Per Principianti:**
- Creazione di un bot Telegram
- Integrazione con Google Sheets API
- Gestione delle dipendenze e ambiente virtuale
- Strutturazione del codice in moduli

**Per Esperti:**
- Implementazione di pattern architetturali
- Gestione avanzata degli errori
- Validazione degli input
- Documentazione del codice

## 🛠️ Installazione

1. **Clona il repository**
   ```bash
   git clone https://github.com/tu-utente/community-chatbot.git
   cd community-chatbot
   ```

2. **Crea un ambiente virtuale (consigliato)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```

3. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configurazione

### 1. Configura il Bot di Telegram
1. Crea un nuovo bot con [@BotFather](https://t.me/botfather) su Telegram
2. Copia il token del bot
3. Crea un file `.env` nella root del progetto e aggiungi:
   ```
   TELEGRAM_BOT_TOKEN=il_tuo_token_qui
   ```

### 2. Configura Google Sheets
1. Vai alla [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto
3. Abilita l'API Google Sheets
4. Crea un account di servizio
5. Scarica il file `credentials.json` e posizionalo nella root del progetto
6. Condividi il tuo foglio Google con l'email dell'account di servizio (con permessi di modifica)

## 🎮 Utilizzo

### Comandi disponibili:

#### `/start`
Avvia il bot e mostra il messaggio di benvenuto.

#### `/spesa` o `/addexpense`
Aggiungi una nuova spesa.

**Sintassi:**
```
/spesa <categoria> <importo> [descrizione]
```

**Esempi:**
```
/spesa cibo 12.50 pranzo
/spesa trasporti 3.00 biglietto autobus
```

## 📊 Struttura del Progetto

```
community-chatbot/
├── bot.py               # Punto di ingresso principale
├── sheets_handler.py    # Gestione Google Sheets
├── requirements.txt     # Dipendenze
├── .env                # Variabili d'ambiente (da creare)
└── README.md           # Questo file
```

## 🔄 Sviluppo

Per contribuire al progetto:

1. Crea un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/nuova-funzionalità`)
3. Fai commit delle tue modifiche (`git commit -am 'Aggiunta nuova funzionalità'`)
4. Pusha il branch (`git push origin feature/nuova-funzionalità`)
5. Crea una Pull Request

## 📝 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 🤝 Contributi

I contributi sono ben accetti! Sentiti libero di aprire una issue o una pull request.
