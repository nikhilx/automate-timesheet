from datetime import datetime, timedelta
from config import config
from auth import ZohoAuth
from typing import Optional
import logging
from timelogger import ZohoTimeLogger

logger = logging.getLogger(__name__)

class TimeLoggerApp:
    def __init__(self):
        self.api_config = config.get_api_config()
        self.auth = ZohoAuth(self.api_config)
        self.time_logger = ZohoTimeLogger(self.api_config)
        self.holidays = config.get_holidays()
        self.leaves = config.get_leaves()

    @classmethod
    def is_weekend(cls, date: datetime) -> bool:
        return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday

    def is_holiday(self, date: datetime) -> bool:
        return date.strftime('%Y-%m-%d') in self.holidays

    def get_skip_reason(self, date: datetime) -> Optional[str]:
        if self.is_weekend(date):
            return "weekend"
        if self.is_holiday(date):
            return "holiday"
        if self.is_leave(date):
            return "leave"
        return None

    def is_leave(self, date: datetime) -> bool:
        return date.strftime('%Y-%m-%d') in self.leaves

    def run(self, preset: Optional[str] = None) -> None:
        timelog_config = config.get_timelog_config(preset)

        access_token = self.auth.get_access_token()
        if not access_token:
            logger.error("Failed to obtain an access token. Exiting.")
            return

        work_date = datetime.strptime(timelog_config['from_date'], '%Y-%m-%d')
        end_date = datetime.strptime(timelog_config['to_date'], '%Y-%m-%d')

        while work_date <= end_date:
            skip_reason = self.get_skip_reason(work_date)

            if skip_reason:
                logger.info(f"Skipped {work_date.strftime('%Y-%m-%d')} due to {skip_reason}.")
            else:
                self.time_logger.add_timelog(
                    access_token,
                    timelog_config['job_id'],
                    timelog_config['hours'],
                    work_date.strftime('%Y-%m-%d'),
                    timelog_config['user'],
                    timelog_config.get('work_item')
                )

            work_date += timedelta(days=1)

        logger.info("Time logging completed.")
