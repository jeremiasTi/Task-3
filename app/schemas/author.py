from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AuthorBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None


class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

