import hashlib
import hmac
import json
import time
import requests
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

api_key = os.getenv('API_KEY_DELTA_INDIA')
api_secret = os.getenv('SECRETE_KEY_DELTA_INDIA')

# Create the signature
def generate_signature(method, endpoint, payload):
    timestamp = str(int(time.time()))
    signature_data = method + timestamp + endpoint + payload
    message = bytes(signature_data, 'utf-8')
    secret = bytes(api_secret, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    return hash.hexdigest(), timestamp

def getDeltaIndiaAPIKey():
    return api_key
