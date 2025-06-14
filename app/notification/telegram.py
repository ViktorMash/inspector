from typing import Optional
import telebot
import time

from app.config.config import settings
from app.schemas import HTTPResponseSchema



class TelegramBot:
    def __init__(self):
        self.dev_list = settings.telegram.dev_recipient_list
        self.managers_list = settings.telegram.manager_recipient_list
        self.send_retries = settings.attempt_retries
        self.bot = telebot.TeleBot(settings.telegram.token, parse_mode='HTML')

    def _send_message(
            self,
            *,
            text: str,
            chat_id: Optional[str] = None,
            disable_notification: bool = False
    ) -> None:
        """ Отправка сообщений в телеграм с обработкой ошибок """

        for attempt in range(self.send_retries):
            try:
                self.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    disable_notification=disable_notification,
                    parse_mode="HTML",
                )
                break
            except Exception as e:
                error_msg = (
                    f"На {attempt + 1} попытке - ошибка отправки в телеграм\n"
                    f"Чат: {chat_id}\n"
                    f"Сообщение: {str(text[:50])}\n"
                    f"Ошибка: {str(e)}"
                )
                print(error_msg)

                if attempt < self.send_retries - 1:
                    time.sleep(settings.polling_sleep)

    def report_managers(self, text: str) -> None:
        """ Репорт разработчикам и манагерам """
        for manager_id in (self.dev_list + self.managers_list):
            self._send_message(text=text, chat_id=manager_id)

    def report_error(self, *, error: str, response: HTTPResponseSchema) -> None:
        """ Репорт об ошибке """
        status_code = response.meta.status_code
        description = response.meta.error

        print(f"{error}: {status_code}\n Текст: {description}")
        err_msg = f"⚠️ <b>{error}</b>: \n\n{description}"
        for dev_id in self.dev_list:
            self._send_message(text=err_msg, chat_id=dev_id)


tg = TelegramBot()

if __name__ == "__main__":

    msg = "Привет"
    u = "465613410"

    tg._send_message(text=msg, chat_id=u)