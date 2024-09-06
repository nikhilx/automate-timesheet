import requests
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class ZohoTimeLogger:
    def __init__(self, api_config: Dict[str, str]):
        self.api_config = api_config

    def add_timelog(self, access_token: str, job_id: str, hours: float, work_date: str, email: str, work_item: Optional[str] = None) -> bool:
        url = f"{self.api_config['zoho_api_domain']}/people/api/timetracker/addtimelog"

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

        if response.status_code == 200:
            logger.info(f"Timelog added successfully for {work_date}")
            return True
        else:
            logger.error(f"Failed to add timelog for {work_date}: {response.status_code}, {response.text}")
            return False