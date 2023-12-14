import os
import requests
from pathlib import Path

def save_output(name: str, value: str): 
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
        print(f'{name}={value}', file=output_file)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_REALM = os.getenv("CLIENT_REALM")
RUN_ID = os.getenv("RUN_ID")

inputs_list = [CLIENT_ID, CLIENT_KEY, CLIENT_REALM, RUN_ID]

if None in inputs_list:
    print("- Some mandatory input is empty. Please, check the input list.")
    exit(1)

idm_url = f"https://idm.stackspot.com/realms/{CLIENT_REALM}/protocol/openid-connect/token"
idm_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
idm_data = { "client_id":f"{CLIENT_ID}", "grant_type":"client_credentials", "client_secret":f"{CLIENT_KEY}" }

r1 = requests.post(
        url=idm_url, 
        headers=idm_headers, 
        data=idm_data
    )

if r1.status_code == 200:
    d1 = r1.json()
    access_token = d1["access_token"]

    cancel_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    cancel_run_url="https://runtime-manager.v1.stackspot.com/v1/run/cancel/{RUN_ID}"
    r2 = requests.post(
            url=cancel_run_url, 
            headers=cancel_headers
        )

    if r2.status_code == 200:
        d2 = r2.json()
        print(f"- RUN {RUN_ID} cancelled successfully!")

    else:
        print("- Error cancelling run")
        print("- Status:", r2.status_code)
        print("- Error:", r2.reason)
        exit(1)

else:
    print("- Error during authentication")
    print("- Status:", r1.status_code)
    print("- Error:", r1.reason)
    exit(1)
