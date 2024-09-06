import configparser
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, config_file: str = './config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.config_file = config_file
        logger.info(f"Loaded configuration from {config_file}")

    def get_api_config(self) -> Dict[str, str]:
        return {
            'client_id': self.config.get('API', 'client_id'),
            'client_secret': self.config.get('API', 'client_secret'),
            'zoho_domain': self.config.get('DEFAULT', 'zoho_domain'),
            'zoho_api_domain': self.config.get('DEFAULT', 'zoho_api_domain'),
            'refresh_token': self.config.get('API', 'refresh_token', fallback=None),
            'auth_code': self.config.get('API', 'auth_code', fallback=None)
        }

    def get_timelog_config(self, preset: str | None = None) -> Dict[str, Any]:
        if preset:
            return self.get_preset(preset)
        else:
            return {
                'from_date': self.config.get('TIMELOG', 'from_date'),
                'to_date': self.config.get('TIMELOG', 'to_date'),
                'job_id': self.config.get('TIMELOG', 'job_id'),
                'hours': self.config.getfloat('TIMELOG', 'hours'),
                'user': self.config.get('TIMELOG', 'user'),
                'work_item': self.config.get('TIMELOG', 'work_item', fallback=None)
            }

    def get_preset(self, preset_name: str) -> Dict[str, Any]:
        today = datetime.now()
        if preset_name == 'weekly':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            date_range = {
                'from_date': start_of_week.strftime('%Y-%m-%d'),
                'to_date': end_of_week.strftime('%Y-%m-%d'),
            }
        elif preset_name == 'monthly':
            start_of_month = today.replace(day=1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            date_range = {
                'from_date': start_of_month.strftime('%Y-%m-%d'),
                'to_date': end_of_month.strftime('%Y-%m-%d'),
            }
        else:
            raise ValueError(f"Unknown preset: {preset_name}")

        return {
            **self.get_timelog_config(),  # Get default timelog config
            **date_range,  # Override with preset date range
            'work_item': self.config.get('PRESETS', f'{preset_name}_work_item', fallback=None)
        }

    def save_refresh_token(self, refresh_token: str) -> None:
        self.config.set('API', 'refresh_token', refresh_token)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        logger.info("Refresh token saved to config file")

    def get_holidays(self):
        return [date.strip() for date in self.config.get('Holidays', 'dates').split(',')]

    def get_leaves(self):
        return [date.strip() for date in self.config.get('Leaves', 'dates').split(',')]

config = Config()