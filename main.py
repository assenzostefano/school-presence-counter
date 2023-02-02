from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import gspread
import os

load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
    ]

credentials = ServiceAccountCredentials.from_json_keyfile_name("token.json", scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open_by_key(SPREADSHEET_ID) #open sheet
# Print value of cell A1
for i in range(1, 10):
    print(sheet.get_worksheet(0).cell(i,1).value)