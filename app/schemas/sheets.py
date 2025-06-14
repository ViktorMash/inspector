from typing import List

from pydantic import Field

from app.schemas._base import BaseSchema


class GridProperties(BaseSchema):
    """ Модель для свойств сетки листа """
    row_count: int = Field(
        default=...,
        alias="rowCount",
        description="Количество строк в листе",
    )
    column_count: int = Field(
        default=...,
        alias="columnCount",
        description="Количество столбцов в листе",
    )


class SheetProperties(BaseSchema):
    """Модель для получения свойств листа"""
    sheet_id: int = Field(
        default=...,
        alias="sheetId",
        description="ID листа в таблице Google Sheets",
    )
    sheet_name: str = Field(
        default=...,
        alias="title",
        description="Название листа в таблице Google Sheets",
    )
    grid_properties: GridProperties = Field(
        alias="gridProperties",
        description="ID листа в таблице Google Sheets",
    )


class Sheet(BaseSchema):
    """ Модель для представления листа """
    properties: SheetProperties


class GetSheetsSchema(BaseSchema):
    """ Модель для получения данных из Google Sheets """
    sheets: List[Sheet]


class ReadSheetSchema(BaseSchema):
    """ Модель для прочитанных данных с листа """

    range: str = Field(
        default=...,
        description="Диапазон",
    )
    dimension: str = Field(
        default=...,
        alias="majorDimension",
        description="COLUMNS | ROWS",
    )
    values: List[List[str]] = Field(
        default=...,
        alias="values",
        description="Данные список в списке",
    )