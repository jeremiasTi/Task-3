from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    author = Author(**data.model_dump())
    db.add(author)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    db.refresh(author)
    return author


@router.get("", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return db.scalars(select(Author).order_by(Author.id)).all()


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return author


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, data: AuthorUpdate, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(author, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    db.refresh(author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    db.delete(author)
    db.commit()

