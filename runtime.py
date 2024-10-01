import os
import requests

def save_output(name: str, value: str):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
        print(f'{name}={value}', file=output_file)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_REALM = os.getenv("CLIENT_REALM")
RUN_ID = os.getenv("RUN_ID")
FORCE = os.getenv("FORCE_CANCEL")


inputs_list = [CLIENT_ID, CLIENT_KEY, CLIENT_REALM]

API_URL = "https://runtime-manager.v1.stackspot.com"

if None in inputs_list:
    print("- Some mandatory input is empty. Please, check the input list.")
    exit(1)
    
if RUN_ID == "":
    print("- RUN_ID was not provided.")
    print("  Deployment was not successfully created.")
    print("  No need to cancel it.")
    exit(0)

print("Authenticating..")
iam_url = f"https://iam-auth-ssr.stg.stackspot.com/{CLIENT_REALM}/oidc/oauth/token"
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

# Calling 
auth_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
cancel_run_url=f"{API_URL}/v1/run/cancel/{RUN_ID}?force=true"


print(f"Requesting Run {RUN_ID} to be cancelled")

try:
    cancel_request = requests.post(
            url=cancel_run_url, 
            headers=auth_headers
        )

    if cancel_request.status_code == 202:
        print(f"- RUN {RUN_ID} cancelled successfully!")

    elif cancel_request.status_code == 404:
        print(f"- RUN {RUN_ID} not found.")

    elif cancel_request.status_code == 422:
        print(f"- RUN {RUN_ID} is already finished, no need to abort")

    else:
        print("- Error cancelling run")
        print("- Status:", cancel_request.status_code)
        print("- Error:", cancel_request.reason)
        exit(1)
finally:
    fetch_run_data_url =  f"{API_URL}/v1/run/{RUN_ID}"

    run_data_req = requests.get(
        headers=auth_headers,
        url=fetch_run_data_url
    )

    if run_data_req.status_code == 200:
        save_output('run_data', run_data_req.text)
    else:
        print("- Error fetching run data, unable to create output")
        print("- Status:", run_data_req.status_code)
        print("- Error:", run_data_req.reason)