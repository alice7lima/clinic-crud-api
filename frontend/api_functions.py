import requests
import json
from config import api_token 
from dotenv import load_dotenv
import os

load_dotenv()
CLINIC_API_BASE_URL = os.getenv('API_BASE_URL')

def do_login(user, password):
    global api_token 
    login_params = {
        "username": user,
        "password": password
    }
    login_url = f"{CLINIC_API_BASE_URL}/login"

    response = requests.post(url=login_url, data=login_params)

    if response.status_code != 200:
        return {"status_code": response.status_code, "msg": response.text}
    
    api_token = json.loads(response.text)["access_token"]
    return api_token 


def create_patient(patient_data):
    global api_token
    if api_token is None:
        do_login(os.getenv("CLINIC_API_USER"), os.getenv("CLINIC_API_PASSOWORD")) 

    headers = {"Authorization": f"Bearer {api_token}"}
    
    patient_url = f"{CLINIC_API_BASE_URL}/patients"
    response = requests.post(url=patient_url, json=patient_data, headers=headers)
    return response


if __name__ == '__main__':
    pass
