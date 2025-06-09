import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
SPREADSHEET_ID = '1lghaMKWcI9Fj_1mv9R2nTDp7S2Wxy1KPceCw8F7DgSM'
CREDENTIALS_FILE = 'credentials.json'  # Make sure this file is in the same directory or provide the correct path
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    """
    Authenticates with Google Sheets API using service account credentials
    and returns a service object.
    """
    creds = None
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        service = build('sheets', 'v4', credentials=creds)
        logger.info("Google Sheets API service created successfully.")
        return service
    except FileNotFoundError:
        logger.error(f"Credentials file '{CREDENTIALS_FILE}' not found. Please ensure it is in the correct path.")
        return None
    except HttpError as err:
        logger.error(f"An API error occurred: {err}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while creating Google Sheets API service: {e}")
        return None

if __name__ == '__main__':
    # Example usage (optional, for testing purposes)
    service = get_sheets_service()
    if service:
        logger.info("Successfully obtained Google Sheets service object.")
        # You can add a simple test call here, e.g., reading a small range
        try:
            sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
            logger.info(f"Spreadsheet Title: {sheet_metadata.get('properties').get('title')}")
        except HttpError as err:
            logger.error(f"An API error occurred while trying to get spreadsheet metadata: {err}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during test call: {e}")
    else:
        logger.warning("Failed to obtain Google Sheets service object.")

def add_row_to_sheet(values: list) -> bool:
    """
    Adds a new row with the given values to the Google Sheet.

    Args:
        values: A list of values to add as a row.
                Example: ["2024-07-30", "Groceries", "50.00", "Weekly shopping"]

    Returns:
        True if the row was added successfully, False otherwise.
    """
    service = get_sheets_service()
    if not service:
        logger.error("Failed to get Google Sheets service. Cannot add row.")
        return False

    try:
        body = {'values': [values]}
        # Assuming the sheet name is 'Sheet1'. This might need to be configurable later.
        # The range 'Sheet1!A1' tells Sheets to find the first empty row in Sheet1 and append there.
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A1',  # Appends to the first table found in 'Sheet1'
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        logger.info(f"Successfully added row. Updates: {result.get('updates')}")
        return True
    except HttpError as error:
        logger.error(f"An API error occurred while adding row: {error}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while adding row: {e}")
        return False

if __name__ == '__main__':
    # Example usage (optional, for testing purposes)
    service = get_sheets_service()
    if service:
        logger.info("Successfully obtained Google Sheets service object.")
        # Test getting spreadsheet metadata
        try:
            sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
            logger.info(f"Spreadsheet Title: {sheet_metadata.get('properties').get('title')}")
        except HttpError as err:
            logger.error(f"An API error occurred while trying to get spreadsheet metadata: {err}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during metadata test call: {e}")

        # Test adding a row
        # IMPORTANT: This test will attempt to write to your Google Sheet if credentials are valid.
        # Ensure 'credentials.json' is present and configured correctly for this test to run.
        logger.info("Attempting to add a sample row to the sheet...")
        sample_row_data = ["2024-01-01", "Test Expense", "10.99", "This is a test entry"]
        if add_row_to_sheet(sample_row_data):
            logger.info("Sample row added successfully (check your Google Sheet).")
        else:
            logger.warning("Failed to add sample row. Check logs for errors (e.g., credentials, API permissions).")
    else:
        logger.warning("Failed to obtain Google Sheets service object. Cannot run tests.")
