from datetime import datetime, timedelta, date
from typing import Tuple, Optional

from app.config import settings
from app.notification.telegram import tg
from app.schemas import HTTPResponseSchema
from app.services import sheets
from app.core import period


class IntalevHandler:
    """ Методы для проверки генерации отчета Инталев """

    HEADER = "Intalev"
    ERROR_HEADER = f"⚠️ {HEADER} ⚠️"

    def __init__(self):

        self.settings = settings.sheets
        self.sheets = sheets
        self.period = period
        self.tg = tg

    def check(self):
        """ Проверить отчет Riki Intalev """
        msg = "\n"
        header = self.HEADER

        if self._is_launch_day():
            check_report_response = self._get_report_data()
            status_code = check_report_response.meta.status_code

            if status_code == 404:  # генерации не было
                header = self.ERROR_HEADER
                msg += check_report_response.meta.error
            elif status_code == 200:
                msg += check_report_response.data["msg"]
            else:  # прочие ошибки
                self.tg.report_error(error="Intalev", response=check_report_response)

            get_report_logs_response = self._get_report_logs()
            status_code = get_report_logs_response.meta.status_code

            if status_code == 404:  # рассылки не было
                header = self.ERROR_HEADER
                msg += f"\n\n{get_report_logs_response.meta.error}"
            elif status_code == 200:
                msg += (
                    f"\n\nРассылка произведена на:"
                    f"\n{'\n'.join([mail for mail in get_report_logs_response.data['recipients'].split(',')])}"
                )
            else:  # прочие ошибки
                self.tg.report_error(error="Intalev", response=check_report_response)

            msg = header + msg
            self.tg.report_managers(msg)

    def _get_report_data(self) -> HTTPResponseSchema:
        """ Сбор данных по генерации Инталев """

        get_sheets_response = self.sheets.get_all_sheets()
        if get_sheets_response.meta.status_code != 200:
            return get_sheets_response

        report_date = self._get_report_date()
        sheet_names = {
            sheet.properties.sheet_name
            for sheet in get_sheets_response.data.sheets
            if "." in sheet.properties.sheet_name
        }
        latest_date = max(sheet_names, key=lambda x: datetime.strptime(x, self.settings.sheet_name_template))
        test_sheet_msg = "\nЛист с именем test не удален" if "test" in sheet_names else ""

        if report_date in sheet_names:
            msg = (
                f"\nГенерация завершена успешно"
                f"\nСоздан лист {report_date}"
                f"{test_sheet_msg}"
            )
            return HTTPResponseSchema.success(
                data={"msg": msg}
            )
        return HTTPResponseSchema.error(
            status_code=404,
            status_description="Отчет не найден",
            error=(
                f"\nОтчет за дату {report_date} не найден"
                f"\nПоследний отчет был {latest_date}"
                f"\n{test_sheet_msg if test_sheet_msg else ''}"
            )
        )

    def _get_report_logs(self) -> HTTPResponseSchema:
        """ Проверка логов Инталев """

        get_sheets_response = self.sheets.read_cols(
            sheet_name=self.settings.riki_logs_sheet_name,
            read_range="A:B"
        )
        if get_sheets_response.meta.status_code != 200:
            return get_sheets_response

        report_date = self._get_report_date()
        logs = get_sheets_response.data.values

        xls_dates = logs[0]
        del xls_dates[0]  # удаляем заголовок 'sheet name'
        xls_recipients = logs[1]
        del xls_recipients[0]  # удаляем заголовок 'email recipients list'

        is_mailed = False  # была ли рассылка в отчетную дату
        recipients = None
        mailing_max_dt = '01.01.2000'
        dt_template = self.settings.sheet_name_template

        for i, dt in enumerate(xls_dates):
            mailing_max_dt = dt \
                if datetime.strptime(dt, dt_template) > datetime.strptime(mailing_max_dt, dt_template) \
                else mailing_max_dt

            if dt == report_date:
                is_mailed = True
                recipients = xls_recipients[i]

        if is_mailed:
            return HTTPResponseSchema.success(
                data={
                    "recipients": recipients
                }
            )

        return HTTPResponseSchema.error(
            status_code=404,
            status_description="Рассылки не было",
            error=(
                f"Сегодня рассылки не было\n"
                f"Последняя дата рассылки {mailing_max_dt}"
            )
        )

    def _get_report_date(self) -> str:
        """ Вычисление отчетной даты для Инталев в формате str dd.mm.yyyy """
        today = self.period.get_current_date()
        is_first_workday_at_month, _ = self._is_first_nonweekend_day()

        # В первый рабочий день генерируем отчет на последний день прошлого месяца
        if is_first_workday_at_month:
            return today.replace(day=1) - timedelta(days=1)

        return today.strftime("%d.%m.%Y")

    def _is_launch_day(self) -> bool:
        """ Проверяет, является ли сегодняшний день, днем генерации отчета """

        today = self.period.get_current_date()
        _, first_nonweekend_day = self._is_first_nonweekend_day()
        launch_weekdays = self.settings.launch_weekday

        # если сегодня один из дней генерации отчета и он не раньше первого рабочего дня в месяце
        if today.isoweekday() in launch_weekdays and today >= first_nonweekend_day:
            return True

        return False

    def _is_first_nonweekend_day(self) -> Tuple[bool, Optional[date]]:
        """
            Находит сегодня первый не weekend день текущего месяца.
            :return ('флаг, что сегодня первый день', 'дату первого дня')
        """
        today = self.period.get_current_date()
        first_working_day = None

        # Находим первый не weekend день в месяце. В январе начинаем поиск с 9-го числа
        first_check_day = 9 if today.month == 1 else 1
        last_check_day = 12

        for day in range(first_check_day, last_check_day):
            check_date = datetime(today.year, today.month, day).date()
            weekday = check_date.isoweekday()

            if weekday not in (6, 7):
                first_working_day = check_date
                break

        if today == first_working_day:
            return True, first_working_day

        return False, first_working_day


intalev_handler = IntalevHandler()
