from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class TokenSchema(BaseModel):
    token_type: str = Field(..., alias="token_type")
    expires_in: int = Field(..., alias="expires_in")
    access_token: str = Field(..., alias="access_token")

    @model_validator(mode="before")
    @classmethod
    def extend_access_token(cls, data):
        data["access_token"] = f'{data.get("token_type", "")} {data.get("access_token", "")}'
        return data

    class Config:
        populate_by_alias = True
        frozen = True


class AuthErrorSchema(BaseModel):
    source: str = Field(..., alias="source")
    error_code: Optional[list] = Field(alias="error_codes", default=None)
    error: str = Field(..., alias="error")
    error_description: str = Field(..., alias="error_description")
    error_uri: Optional[str] = Field(alias="error_uri", default=None)
    timestamp: Optional[datetime] = Field(..., alias="timestamp", default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_alias = True
        frozen = True
