from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    isbn: str = Field(min_length=10, max_length=20)
    published_year: int = Field(ge=0, le=2100)


class BookCreate(BookBase):
    author_id: int = Field(gt=0)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    isbn: str | None = Field(default=None, min_length=10, max_length=20)
    published_year: int | None = Field(default=None, ge=0, le=2100)
    author_id: int | None = Field(default=None, gt=0)


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
