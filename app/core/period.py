from datetime import date, datetime
from typing import Optional, Union
from tzlocal import get_localzone

from app.config import settings


class DefineDates:
    def __init__(self):
        self.main_settings = settings

    def now(self) -> str:
        """ Текущая дата и время для логов """
        return self.get_current_date().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def get_current_date(*, is_string: Optional[bool] = False) -> Union[date, str]:
        """ Возвращает текущую дату в формате date или dd.mm.yyyy"""
        today = date.today()
        if is_string:
            return today.strftime("%d.%m.%Y")
        return today

    def launch_time(self, hour: int, minute: int) -> str:
        """
            генерация времени запуска scheduler с учетом времени сервера
            не обрабатывает время с 00:00 - 03:00
        """
        offset = self._get_offset()
        text_hour = f'0{hour - offset}' if hour - offset < 10 else hour - offset
        text_minute = f'0{minute}' if minute < 10 else minute
        text_time = f'{text_hour}:{text_minute}'

        return text_time

    def _get_offset(self) -> int:
        """ время запуска с учетом времени сервера """
        server_timezone = get_localzone()
        server_time = datetime.now(server_timezone)
        utc_offset = int(server_time.utcoffset().total_seconds() / 3600)
        time_offset = self.main_settings.gmt_time_zone - utc_offset
        return time_offset


period = DefineDates()
