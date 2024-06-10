from uuid import UUID

from pydantic import BaseModel


class RegionsError(BaseModel):
    error: 'RegionsErrorInfo'


class RegionsErrorInfo(BaseModel):
    id: UUID
    message: str
