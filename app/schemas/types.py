from typing import TypeVar

from app.schemas.sheets import GetSheetsSchema


GenericType = TypeVar('GenericType')


GoogleSheetsTypes = TypeVar(
    'GoogleSheetsTypes',
    bound=GetSheetsSchema
)
