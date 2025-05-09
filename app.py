from flask import Flask, jsonify, request
from google.oauth2 import service_account
import google.auth.transport.requests
import os

app = Flask(__name__)

# API key should be set as an environment variable
API_KEY = os.getenv('API_KEY')

def require_api_key(f):
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({'error': 'Unauthorized'}), 401
    decorated.__name__ = f.__name__
    return decorated

@app.route('/get-google-token', methods=['GET'])
@require_api_key
def get_token():
    SERVICE_ACCOUNT_FILE = '/etc/secrets/account_service_credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/drive',
              "https://spreadsheets.google.com/feeds"]

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    access_token = creds.token

    return jsonify({'access_token': access_token})

if __name__ == '__main__':
    app.run(debug=True)
