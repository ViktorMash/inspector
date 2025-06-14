from pydantic import BaseModel


class BaseSchema(BaseModel):
    """ Базовая схема """
    pass

    class Config:
        populate_by_name=True
        arbitrary_types_allowed=True
