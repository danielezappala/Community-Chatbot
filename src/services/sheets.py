"""
Modulo per la gestione dell'integrazione con Google Sheets.

Questo servizio si occupa di tutte le operazioni di lettura e scrittura
sul foglio di calcolo Google utilizzato per il tracciamento delle spese.
"""
import logging
import os
import json
import time
from pathlib import Path
from typing import List, Any, Dict, Optional, Tuple, Union

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient import discovery, errors
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

# Carica le variabili d'ambiente da .env
load_dotenv()

# Configurazione del logger per questo modulo
logger = logging.getLogger(__name__)

# Costanti per la configurazione del foglio
DEFAULT_SHEET_NAME = 'Sheet1'
DEFAULT_SHEET_RANGE = f'{DEFAULT_SHEET_NAME}!A:E'
DEFAULT_VALUE_INPUT_OPTION = 'USER_ENTERED'
MAX_RETRIES = 3
RETRY_DELAY = 2  # secondi


class ConfigError(Exception):
    """Eccezione sollevata quando mancano configurazioni richieste."""
    pass


def get_required_env_var(name: str) -> str:
    """Recupera una variabile d'ambiente richiesta o solleva un'eccezione."""
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"La variabile d'ambiente {name} è richiesta ma non è stata impostata")
    return value


# Costanti per la configurazione del foglio
DEFAULT_SHEET_RANGE = 'Sheet1!A:E'
DEFAULT_VALUE_INPUT_OPTION = 'USER_ENTERED'

class SheetsService:
    """
    Servizio per l'interazione con Google Sheets API.
    
    Questa classe fornisce metodi per interagire con un foglio di calcolo Google,
    in particolare per l'aggiunta di nuove voci di spesa.
    """
    
    def __init__(self, spreadsheet_id: str = None, 
                 credentials_path: str = None) -> None:
        """
        Inizializza il servizio Google Sheets.
        
        Args:
            spreadsheet_id: ID del foglio di calcolo Google.
                          Se None, viene usato il valore da GOOGLE_SHEETS_SPREADSHEET_ID.
            credentials_path: Percorso al file delle credenziali JSON.
                           Se None, viene usato il valore da GOOGLE_SHEETS_CREDENTIALS_JSON.
        """
        # Inizializza il logger
        self.logger = logging.getLogger(__name__)
        
        try:
            # Configura l'ID del foglio
            self.spreadsheet_id = spreadsheet_id or get_required_env_var('GOOGLE_SHEETS_SPREADSHEET_ID')
            
            # Configura il percorso delle credenziali
            credentials_path = credentials_path or get_required_env_var('GOOGLE_SHEETS_CREDENTIALS_JSON')
            
            # Verifica che il file delle credenziali esista
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"File delle credenziali non trovato: {credentials_path}. "
                    f"Assicurati che il percorso sia corretto e che il file esista."
                )
            
            # Carica le credenziali dal file JSON
            self.logger.debug(f"Caricamento credenziali da: {credentials_path}")
            creds = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Inizializza il servizio
            self.service = discovery.build('sheets', 'v4', credentials=creds)
            self.logger.info("Servizio Google Sheets inizializzato con successo")
            
        except ConfigError as e:
            self.logger.error(f"Errore di configurazione: {e}")
            raise
        except FileNotFoundError as e:
            self.logger.error(str(e))
            raise
        except Exception as e:
            self.logger.error(f"Errore durante l'inizializzazione del servizio Google Sheets: {e}")
            raise

    def _execute_with_retry(self, api_call, *args, **kwargs):
        """
        Esegue una chiamata API con meccanismo di ripetizione in caso di errore.
        
        Args:
            api_call: Funzione da eseguire
            *args, **kwargs: Argomenti da passare alla funzione
            
        Returns:
            Il risultato della chiamata API
            
        Raises:
            Exception: Se tutte le ripetizioni falliscono
        """
        last_exception = None
        
        for attempt in range(MAX_RETRIES):
            try:
                return api_call(*args, **kwargs).execute()
            except (HttpError, errors.Error) as e:
                last_exception = e
                if attempt < MAX_RETRIES - 1:  # Non attendere dopo l'ultimo tentativo
                    wait_time = RETRY_DELAY * (2 ** attempt)  # Backoff esponenziale
                    self.logger.warning(
                        f"Tentativo {attempt + 1} fallito. Riprovo tra {wait_time} secondi..."
                    )
                    time.sleep(wait_time)
        
        # Se arriviamo qui, tutti i tentativi sono falliti
        self.logger.error(
            f"Tutti i {MAX_RETRIES} tentativi falliti. Ultimo errore: {last_exception}",
            exc_info=True
        )
        raise last_exception
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Verifica la connessione al foglio di calcolo.
        
        Returns:
            Tuple[bool, str]: (successo, messaggio)
        """
        try:
            # Prova a ottenere i metadati del foglio
            spreadsheet = self._execute_with_retry(
                self.service.spreadsheets().get,
                spreadsheetId=self.spreadsheet_id
            )
            title = spreadsheet.get('properties', {}).get('title', 'Sconosciuto')
            return True, f"Connessione riuscita al foglio: {title}"
            
        except HttpError as http_err:
            error_msg = f"Errore HTTP {http_err.resp.status}: {http_err}"
            self.logger.error(error_msg, exc_info=True)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Errore durante la connessione: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return False, error_msg
    
    def add_expense(self, row_data: List[Any]) -> bool:
        """
        Aggiunge una nuova riga di spesa al foglio di calcolo.
        
        Args:
            row_data: Lista contenente i dati della spesa nel seguente ordine:
                     [data, utente, categoria, importo, descrizione]
                     
        Returns:
            bool: True se l'operazione è andata a buon fine, False altrimenti.
            
        Example:
            >>> service = SheetsService()
            >>> service.add_expense(["2023-01-01", "mario", "Cibo", "12.50", "Pranzo"])
            True
        """
        try:
            # Validazione dei dati in ingresso
            if not isinstance(row_data, (list, tuple)) or len(row_data) < 5:
                self.logger.error(f"Formato dati non valido: {row_data}")
                return False
                
            # Prepara i dati per la formattazione
            formatted_row = [
                row_data[0],  # data
                row_data[1],  # utente
                row_data[2],  # categoria
                float(row_data[3]) if isinstance(row_data[3], (int, float, str)) and str(row_data[3]).replace('.', '', 1).isdigit() else 0,  # importo
                str(row_data[4]) if len(row_data) > 4 else ''  # descrizione
            ]
            
            # Prepara il corpo della richiesta per l'API
            body = {
                'values': [formatted_row],
                'majorDimension': 'ROWS'
            }
            
            # Esegue la chiamata all'API con meccanismo di ripetizione
            result = self._execute_with_retry(
                self.service.spreadsheets().values().append,
                spreadsheetId=self.spreadsheet_id,
                range=DEFAULT_SHEET_RANGE,
                valueInputOption=DEFAULT_VALUE_INPUT_OPTION,
                insertDataOption='INSERT_ROWS',
                body=body
            )
            
            # Log dell'operazione riuscita con dettagli
            updates = result.get('updates', {})
            self.logger.info(
                f"Spesa aggiunta con successo. "
                f"Aggiornate {updates.get('updatedCells', 0)} celle. "
                f"Range aggiornato: {updates.get('updatedRange', 'sconosciuto')}"
            )
            return True
            
        except Exception as e:
            self.logger.error(
                f"Errore durante l'aggiunta della spesa: {str(e)}",
                exc_info=True
            )
            return False
