import os
from flask import Flask
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# mpesa details
MPESA_KEY = os.environ['MPESA_KEY']
MPESA_SECRET = os.environ['MPESA_SECRET']


@app.route("/")
def home():
    return "Hello World!"


# access token
@app.route("/access_token")
def token():
    data = ac_token()
    return data


def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(MPESA_KEY, MPESA_SECRET))

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": "Failed to get access token"}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3400, debug=True)
