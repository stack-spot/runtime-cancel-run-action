import os
import requests

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_REALM = os.getenv("CLIENT_REALM")
RUN_ID = os.getenv("RUN_ID")

inputs_list = [CLIENT_ID, CLIENT_KEY, CLIENT_REALM, RUN_ID]

print("Run Id: ",RUN_ID)
print("Type", type(RUN_ID))

if None in inputs_list:
    print("- Some mandatory input is empty. Please, check the input list.")
    exit(1)

# Getting access token
print("Authenticating..")
iam_url = f"https://auth.stackspot.com/{CLIENT_REALM}/oidc/oauth/token"
iam_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
iam_data = { "client_id":f"{CLIENT_ID}", "grant_type":"client_credentials", "client_secret":f"{CLIENT_KEY}" }

login_req = requests.post(
        url=iam_url, 
        headers=iam_headers, 
        data=iam_data
    )

if login_req.status_code != 200:
    print("- Error during iam authentication")
    print("- Status:", login_req.status_code)
    print("- Error:", login_req.reason)
    print("- Response:", login_req.text)
    exit(1) 

d1 = login_req.json()
access_token = d1["access_token"]

# Calling Cancel Action
print("Cancelling Run...")
cancel_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
cancel_run_url=f"https://runtime-manager.v1.stackspot.com/v1/run/cancel/{RUN_ID}"

cancel_request = requests.post(
        url=cancel_run_url, 
        headers=cancel_headers
    )

if cancel_request.status_code == 202:
    print(f"- RUN {RUN_ID} cancelled successfully!")

elif cancel_request.status_code == 404:
    print(f"- RUN {RUN_ID} not found.")

elif cancel_request.status_code == 422:
    print(f"- RUN {RUN_ID} not currently running. Unable to Abort.")

else:
    print("- Error cancelling run")
    print("- Status:", cancel_request.status_code)
    print("- Error:", cancel_request.reason)
    print("- Response:", cancel_request.text)
    exit(1)
