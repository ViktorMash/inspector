from app.config import settings
from app.http.google_sheets import google_sheets_client
from app.schemas import ReadSheetSchema, HTTPResponseSchema
from app.schemas import GetSheetsSchema

from pprint import pprint


class GoogleSheetsHandler:
    """ Работа с Google Sheets API """

    def __init__(self):

        self.client = google_sheets_client
        self.google_config = settings.sheets

    def read_cols(
        self,
        *,
        sheet_name: str,
        read_range: str
    ) -> HTTPResponseSchema:
        """
            Чтение данных
            Args:
                sheet_name: имя листа
                read_range: диапазон ячеек для чтения
        """
        range_value = f'{sheet_name}!{read_range}'
        dimension_value = "COLUMNS"

        request = self.client.get_values(
            spreadsheetId=self.google_config.riki_spreadsheet_id,
            range=range_value,
            majorDimension=dimension_value
        )
        return self.client.api_request(
            request=request,
            model=ReadSheetSchema
        )

    def get_all_sheets(self) -> HTTPResponseSchema[GetSheetsSchema]:
        """ Получить все листы """
        request = self.client.get(
            spreadsheetId=self.google_config.riki_spreadsheet_id,
            includeGridData=False
        )
        return self.client.api_request(
            request=request,
            model=GetSheetsSchema
        )


sheets = GoogleSheetsHandler()


if __name__ == "__main__":
    # Пример использования
    '''
    response = google_sheets.read_rows(
        sheet_name="07.05.2025",
        read_range="A1:B10"
    )
    '''
    response = sheets.get_all_sheets()
    pprint(response)