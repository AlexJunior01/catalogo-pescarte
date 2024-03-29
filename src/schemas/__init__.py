from pydantic import BaseModel, UUID4, validator
import enum


class ErrorMessage(BaseModel):
    message: str


class SuggestCommonNameBody(BaseModel):
    name: str
    email: str
    uf: str
    fish_id: UUID4
    community_id: UUID4
    suggested_name: str


class SuggestedCommonNameResponse(BaseModel):
    id: UUID4
    name: str
    email: str
    suggested_name: str
    status: str
    fish_id: UUID4
    community_id: UUID4

    @validator('status', pre=True, always=True)
    def convert_status_to_string(cls, value):
        if isinstance(value, enum.Enum):
            return value.value
        return value

    class Config:
        orm_mode = True


class UFSchema(BaseModel):
    uf: str
    uf_name: str

    class Config:
        orm_mode = True


class CitySchema(BaseModel):
    id: UUID4
    uf: str
    name: str

    class Config:
        orm_mode = True
