"""
Service per l'integrazione con Google Sheets
"""
import logging
from googleapiclient import discovery

class SheetsService:
    def __init__(self, spreadsheet_id='1lghaMKWcI9Fj_1mv9R2nTDp7S2Wxy1KPceCw8F7DgSM'):
        self.spreadsheet_id = spreadsheet_id
        self.service = discovery.build('sheets', 'v4')
        self.logger = logging.getLogger(__name__)

    def add_expense(self, row_data):
        """Aggiunge una riga di spesa al foglio"""
        try:
            range_name = 'Sheet1!A:E'
            value_input_option = 'USER_ENTERED'
            body = {'values': [row_data]}
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            
            self.logger.info(f"Riga aggiunta: {result}")
            return True
        except Exception as e:
            self.logger.error(f"Errore Sheets API: {str(e)}")
            return False
