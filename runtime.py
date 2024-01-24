import os
import requests

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_REALM = os.getenv("CLIENT_REALM")
RUN_ID = os.getenv("RUN_ID")

inputs_list = [CLIENT_ID, CLIENT_KEY, CLIENT_REALM, RUN_ID]

print("Run Id: ", RUN_ID, ".")
print("Type: ", type(RUN_ID), ".")

if None in inputs_list:
    print("- Some mandatory input is empty. Please, check the input list.")
    exit(1)

# Accessing keycloak token in order to gain access to account-api

idm_url = f"https://account-keycloak.stg.stackspot.com/realms/{CLIENT_REALM}/protocol/openid-connect/token"
idm_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
idm_data = { "client_id":f"{CLIENT_ID}", "grant_type":"client_credentials", "client_secret":f"{CLIENT_KEY}" }

login_req = requests.post(
        url=idm_url, 
        headers=idm_headers, 
        data=idm_data
    )

if login_req.status_code != 200:
    print("- Error during authentication")
    print("- Status:", login_req.status_code)
    print("- Error:", login_req.reason)
    exit(1) 
    

d1 = login_req.json()
access_token = d1["access_token"]

# Impersonating Token to verify needed permissions

pat_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
pat_url = f"https://account-account-api.stg.stackspot.com/v1/authentication/personal-access-token-sa"

pat_request = requests.post(
        url = pat_url,
        headers=pat_headers,
    )

if pat_request.status_code != 200:
    print("- Error during authentication")
    print("- Status:", pat_request.status_code)
    print("- Error:", pat_request.reason)
    exit(1) 

pat_token= pat_request.json()["accessToken"]

# Calling 

cancel_headers = {"Authorization": f"Bearer {pat_token}", "Content-Type": "application/json"}
cancel_run_url=f"https://runtime-manager.stg.stackspot.com/v1/run/cancel/{RUN_ID}"

cancel_request = requests.post(
        url=cancel_run_url, 
        headers=cancel_headers
    )

if cancel_request.status_code == 202:
    print(f"- RUN {RUN_ID} cancelled successfully!")

elif cancel_request.status_code == 404:
    print(f"- RUN {RUN_ID} not found.")

else:
    print("- Error cancelling run")
    print("- Status:", cancel_request.status_code)
    print("- Error:", cancel_request.reason)
    exit(1)
