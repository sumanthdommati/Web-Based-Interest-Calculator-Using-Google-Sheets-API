from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from flask_cors import CORS
app = Flask(__name__)

CORS(app) 

SPREADSHEET_ID = '13kDn6Y9mFhAGYTySbDQypfXJfX-qJHSobbdjqtiUFS8'  
RANGE_NAME_INPUT = 'Input!B2:B4'  
RANGE_NAME_OUTPUT = 'Output!A1:A2'  

def get_service():
    creds = Credentials.from_service_account_file('credentials.json')  
    service = build('sheets', 'v4', credentials=creds)
    return service

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        principal = data['principal']
        rate = data['rate']
        time = data['time']

        values = [
            [principal],
            [rate],
            [time]
        ]

        service = get_service()
        body = {'values': values}
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME_INPUT,
            valueInputOption='RAW',
            body=body
        ).execute()

        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME_OUTPUT
        ).execute()
        output_values = result.get('values', [])

        response = {
            'simple_interest': output_values[0][0], 
            'compound_interest': output_values[1][0]  
        }
        return jsonify(response)

    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=False)

