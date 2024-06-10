from pydantic import BaseModel


class RegionsResponse(BaseModel):
    total: int
    items: list['RegionsItem']


class RegionsItem(BaseModel):
    id: int
    name: str
    code: str
    country: 'RegionsCountry'


class RegionsCountry(BaseModel):
    name: str
    code: str
