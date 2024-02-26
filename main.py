import os
from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# mpesa details
MPESA_KEY = os.environ['MPESA_KEY']
MPESA_SECRET = os.environ['MPESA_SECRET']
SHORTCODE = os.environ['SHORTCODE']
BASE_URL = os.environ['BASE_URL']


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


# register urls
@app.route("/register_urls")
def register():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": f"Bearer {ac_token()}"}
    req_body = {
        "ShortCode": SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": BASE_URL + "/c2b/confirm",
        "ValidationURL": BASE_URL + "/c2b/validation"
    }

    response_data = requests.post(
        url=mpesa_endpoint,
        json=req_body,
        headers=headers
    )

    return response_data.json()


@app.route("/c2b/confirm")
def confirm():
    # get data
    data = request.json

    # write to file
    with open("confirm.json", "a") as file:
        file.write(data)


@app.route("/c2b/validation")
def validation():
    # get data
    data = request.json

    # write to file
    with open("confirm.json", "a") as file:
        file.write(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3400, debug=True)
