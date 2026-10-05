from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.author import Author


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    published_year: Mapped[int] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True)
    author: Mapped["Author"] = relationship(back_populates="books")

