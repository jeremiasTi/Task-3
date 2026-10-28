from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.author import Author
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


def ensure_author(db: Session, author_id: int) -> None:
    if not db.get(Author, author_id):
        raise HTTPException(status_code=404, detail="Autor não encontrado")


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    ensure_author(db, data.author_id)
    book = Book(**data.model_dump())
    db.add(book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN já cadastrado")
    db.refresh(book)
    return book


@router.get("", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.scalars(select(Book).order_by(Book.id)).all()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    values = data.model_dump(exclude_unset=True)
    if "author_id" in values:
        ensure_author(db, values["author_id"])
    for key, value in values.items():
        setattr(book, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="ISBN já cadastrado")
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(book)
    db.commit()


@router.get("/author/{author_id}", response_model=list[BookResponse])
def list_books_by_author(author_id: int, db: Session = Depends(get_db)):
    ensure_author(db, author_id)

    consulta = select(Book).where(Book.author_id == author_id)
    consulta = consulta.order_by(Book.id)

    livros = db.scalars(consulta).all()

    return livros

