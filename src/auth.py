import requests
from typing import Optional, Dict
from urllib.parse import urlencode
import logging
from config import config

logger = logging.getLogger(__name__)


class ZohoAuth:
    def __init__(self, api_config: Dict[str, str]):
        self.api_config = api_config

    def get_access_token(self) -> Optional[str]:
        if self.api_config.get('refresh_token'):
            return self._get_access_token_via_refresh_token()
        elif self.api_config.get('auth_code'):
            return self._get_access_token_via_auth_code()
        else:
            logger.error("No refresh token or auth code available. Please set up initial authentication.")
            return None

    def _get_access_token_via_refresh_token(self) -> Optional[str]:
        token_url = f"{self.api_config['zoho_domain']}/oauth/v2/token"

        payload = {
            'refresh_token': self.api_config['refresh_token'],
            'client_id': self.api_config['client_id'],
            'client_secret': self.api_config['client_secret'],
            'grant_type': 'refresh_token'
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(token_url, data=urlencode(payload), headers=headers)

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            logger.error(f"Failed to fetch token using refresh token: {response.status_code}, {response.text}")
            return None

    def _get_access_token_via_auth_code(self) -> Optional[str]:
        token_url = f"{self.api_config['zoho_domain']}/oauth/v2/token"

        payload = {
            'code': self.api_config['auth_code'],
            'client_id': self.api_config['client_id'],
            'client_secret': self.api_config['client_secret'],
            'grant_type': 'authorization_code'
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(token_url, data=urlencode(payload), headers=headers)

        if response.status_code == 200:
            data = response.json()
            refresh_token = data.get('refresh_token')
            if refresh_token:
                config.save_refresh_token(refresh_token)
            return data.get('access_token')
        else:
            logger.error(f"Failed to fetch token using auth code: {response.status_code}, {response.text}")
            return None