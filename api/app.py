from flask import Flask, jsonify, render_template
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

app = Flask(__name__)
CORS(app)

# Remove this line since we won't use a file anymore
# SERVICE_ACCOUNT_FILE = 'credentials.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '1UiPzEXZbW8TXwkqEIYleZnbSw2KNHWiAR16jqUfXNQw'
RANGE_NAME = 'Leaderboard!A1:F100'

@app.route('/')
def home():
    return render_template('leaderboard.html')

@app.route('/leaderboard')
def get_leaderboard():
    # Read the JSON string from the environment variable
    json_str = os.environ.get('GOOGLE_SERVICE_ACCOUNT')
    if not json_str:
        return jsonify({"error": "Service account credentials not found in environment variables"}), 500

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(json_str)

    # Create credentials from the dictionary (not from a file)
    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return jsonify(values)

def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
