import json
from typing import List, Set, Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.config.cfg_power_bi import PowerBIAPISettings


dotenv_path = str(Path(__file__).resolve().parent.parent.parent / ".env")
load_dotenv(dotenv_path)


class LicensesKZSettings(BaseSettings):
    """ Лицензии KZ для Riki """
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        description="Default User-Agent header for all requests"
    )
    shop_url: AnyHttpUrl = Field(
        default="",
        description="URL of the microsoft PowerBI KZ licences page"
    )

    model_config = SettingsConfigDict(
        env_prefix="RIKI_LICENCES__"
    )


class GoogleSheetsSettings(BaseSettings):
    """
        Google Sheets для Riki
        https://docs.google.com/spreadsheets/d/1OupD10qLMHr7LwgVFZ9d05ec6h5V0ETkVPoffO40YaI/edit#gid=1724275225
        pip install oauth2client google-api-python-client
    """
    service_account: str = ""
    api_name: str = ""
    api_version: str = ""
    scopes: List[str] = Field(default_factory=list) # Для чтения и записи # Для доступа к Drive API
    riki_spreadsheet_id: str = ""  # id - actual_example
    riki_logs_sheet_name: str = ""
    sheet_name_template: str = "%d.%m.%Y"
    sleep: int = 1
    launch_weekday: Set[int] = {1,3,5}

    model_config = SettingsConfigDict(
        env_prefix="GOOGLE_SHEETS__"
    )

    def get_service_account_info(self) -> Optional[Dict[str, Any]]:
        """Возвращает словарь с учетными данными из JSON-строки"""
        if not self.service_account:
            return None

        try:
            return json.loads(self.service_account)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка при парсинге JSON из переменной окружения: {e}")


class TelegramSettings(BaseSettings):
    token: str = ""  # bot_name: mvs_inspector_bot
    manager_recipient_list: List[int] = Field(default_factory=list)
    dev_recipient_list: List[int] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_prefix="TELEGRAM__"
    )


class Settings(BaseSettings):
    timeout: int = 30
    attempt_retries: int = 5  # количество попыток отправить сообщение, получить токен...
    polling_sleep: int = 3
    gmt_time_zone: int = 3  # временная зона в которой работает scheduler

    power_bi: PowerBIAPISettings = PowerBIAPISettings()
    licenses_kz: LicensesKZSettings = LicensesKZSettings()
    sheets: GoogleSheetsSettings = GoogleSheetsSettings()
    telegram: TelegramSettings = TelegramSettings()

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_nested_delimiter="__"
    )


settings = Settings()
