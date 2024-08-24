import json
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
from dotenv import load_dotenv, set_key
import os

env_path = '.env'
load_dotenv(dotenv_path=env_path)

config = {}


def load_config():
    global config
    with open("config.json") as config_file:
        config = json.load(config_file)


# Function to fetch access token using authorization code
def get_access_token_via_authorization_code():
    zoho_domain = os.getenv('ZOHO_DOMAIN')
    token_url = f"{zoho_domain}/oauth/v2/token"

    payload = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'code': os.getenv('AUTHORIZATION_CODE'),
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=urlencode(payload), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')

        if refresh_token:
            # Save refresh token to .env file
            save_refresh_token(refresh_token)

        return access_token
    else:
        print(f"Failed to fetch token using authorization code: {response.status_code}, {response.text}")
        return None


# Function to fetch access token using refresh token
def get_access_token_via_refresh_token():
    zoho_domain = os.getenv('ZOHO_OAUTH_DOMAIN')
    token_url = f"{zoho_domain}/oauth/v2/token"

    payload = {
        'refresh_token': os.getenv('REFRESH_TOKEN'),
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'grant_type': 'refresh_token'
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=urlencode(payload), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get('access_token')
    else:
        print(f"Failed to fetch token using refresh token: {response.status_code}, {response.text}")
        return None

def add_timelog(access_token, job_id, hours, work_date, email, work_item=None):
    url = "https://people.zoho.com/people/api/timetracker/addtimelog"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'user': email,
        'workDate': work_date,
        'jobId': job_id,
        'hours': hours,
    }

    if work_item:
        params['workItem'] = work_item

    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:  # Check for success status code
        print("Timelog added successfully.")
    else:
        print(f"Failed to add timelog: {response.status_code}, {response.text}")


# Function to save the refresh token to the .env file
def save_refresh_token(refresh_token):
    # Update the .env file with the new refresh token
    set_key(env_path, 'REFRESH_TOKEN', refresh_token)
    print(f"Refresh token saved to .env file: {refresh_token}")


# Main execution
if __name__ == "__main__":
    # Load configuration
    load_config()

    # Fetch access token
    access_token = None
    refresh_token = os.getenv('REFRESH_TOKEN')

    if refresh_token:
        access_token = get_access_token_via_refresh_token()
    else:
        # First time flow: Get token using authorization code
        access_token = get_access_token_via_authorization_code()

    if access_token:
        work_date = datetime.strptime(config['fromDate'], '%Y-%m-%d')
        to_date = datetime.strptime(config['toDate'], '%Y-%m-%d')

        # Loop through dates and add timelogs for each day
        while work_date <= to_date:
            add_timelog(access_token, config['jobId'], config['hours'], work_date.strftime('%Y-%m-%d'), config['user'])
            work_date += timedelta(days=1)
    else:
        print("Failed to obtain an access token. Timelogs will not be added.")
