from flask import Flask, jsonify, render_template
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

# Load Google Sheets credentials
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '1UiPzEXZbW8TXwkqEIYleZnbSw2KNHWiAR16jqUfXNQw'
RANGE_NAME = 'Leaderboard!A1:F100'

@app.route('/')
def home():
    return render_template('leaderboard.html')

@app.route('/leaderboard')
def get_leaderboard():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return jsonify(values)

if __name__ == '__main__':
    app.run(debug=True)
