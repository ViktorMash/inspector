from typing import Dict, Any, Generic, Optional

from pydantic import Field, field_validator
from fastapi import status

from app.schemas._base import BaseSchema
from .types import GenericType


class HTTPResponseMetaData(BaseSchema):
    """ Метаданные HTTP ответа """
    status_code: int = Field(
        default=status.HTTP_200_OK,
        description="HTTP статус"
    )
    status_description: str = Field(
        default="OK",
        description="Описание статуса"
    )
    error: str = Field(
        default=None,
        description="Описание ошибки"
    )
    @field_validator('error', mode='before')
    @classmethod
    def ensure_string_error(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if not isinstance(v, str):
            return str(v)
        return v


class HTTPResponseSchema(BaseSchema, Generic[GenericType]):
    """ Модель HTTP ответов """
    data: Any = Field(
        default_factory=dict,
        description="HTTP ответ. Словарь, список словарей или любая схема в случае успешного запроса"
    )
    meta: HTTPResponseMetaData = Field(
        default_factory=HTTPResponseMetaData,
        description="Метаданные HTTP ответа"
    )

    @classmethod
    def error(
        cls,
        *,
        status_code: int,
        status_description: str,
        error: Any
    ):
        """ Ответ с ошибкой """
        return cls(
            meta=HTTPResponseMetaData(
                status_code=status_code,
                status_description=status_description,
                error=error
            )
        )

    @classmethod
    def success(
        cls,
        *,
        data: Dict[str, Any]
    ):
        """ Успешный ответ """
        return cls(
            data=data
        )
