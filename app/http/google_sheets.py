import time
from typing import Any, Optional

from fastapi import status

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as AuthRequest
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest

from app.config import settings
from app.schemas import HTTPResponseSchema, GoogleSheetsTypes


# todo исключения не обрабатываются корректно
# todo объединить с http_client
class GoogleSheetsClient:
    """ Работа с Google Sheets API """

    def __init__(self):
        # Setup authentication
        self.credentials = service_account.Credentials.from_service_account_info(
            settings.sheets.get_service_account_info(),
            scopes=settings.sheets.scopes
        )
        # Создание API сервиса
        self.service = build(
            settings.sheets.api_name,
            settings.sheets.api_version,
            credentials=self.credentials
        ).spreadsheets()

        # Создание методов для работы с API
        self.get_values = self.service.values().get
        self.get = self.service.get
        self.values_update = self.service.values().batchUpdate
        self.update = self.service.batchUpdate

        # Настройки
        self.sleep = settings.sheets.sleep
        self.max_retries = settings.attempt_retries

    def api_request(
        self,
        *,
        request: HttpRequest,
        model: Optional[GoogleSheetsTypes] = None
    ) -> HTTPResponseSchema[Any]:
        """ Выполнение запросов к Google sheets API"""
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.sleep)
                try:
                    # Если токен устарел, обновляем его
                    if self.credentials.expired:
                        auth_req = AuthRequest()
                        self.credentials.refresh(auth_req)

                    response = request.execute()

                    if model:
                        return HTTPResponseSchema.success(
                            data=model.model_validate(response)
                        )
                    return HTTPResponseSchema.success(
                            data=response
                        )
                except HttpError as e:
                    return HTTPResponseSchema.error(
                        status_code=e.status_code,
                        status_description="Ошибка при обработке HTTP ответа",
                        error=e.error_details
                    )

            except ConnectionError as e:  # todo Timeout or Connection
                err_msg = "Ошибка подключения к Google Sheets API"
                if attempt < self.max_retries - 1:
                    print(f'На {attempt + 1} попытке: {err_msg}')
                    time.sleep(settings.polling_sleep)
                    continue

                return HTTPResponseSchema.error(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    status_description=err_msg,
                    error=str(e)
                )

            except Exception as e:
                return HTTPResponseSchema.error(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    status_description="Внутренняя ошибка",
                    error=str(e)
                )

        return HTTPResponseSchema.error(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_description="Превышено количество попыток подключения",
            error="Maximum retries exceeded"
        )


google_sheets_client = GoogleSheetsClient()
