
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate


router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


@router.post(
    "",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    novo_autor = Author(**data.model_dump())

    try:
        db.add(novo_autor)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado"
        )

    db.refresh(novo_autor)
    return novo_autor


@router.get("", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    consulta = select(Author)
    consulta = consulta.order_by(Author.id)

    autores = db.scalars(consulta).all()

    return autores


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    autor_encontrado = db.get(Author, author_id)

    if autor_encontrado is None:
        raise HTTPException(
            status_code=404,
            detail="Autor não encontrado"
        )

    return autor_encontrado


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    author_id: int,
    data: AuthorUpdate,
    db: Session = Depends(get_db)
):
    autor_atual = db.get(Author, author_id)

    if autor_atual is None:
        raise HTTPException(
            status_code=404,
            detail="Autor não encontrado"
        )

    campos_atualizados = data.model_dump(exclude_unset=True)

    for campo in campos_atualizados:
        setattr(autor_atual, campo, campos_atualizados[campo])

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado"
        )

    db.refresh(autor_atual)

    return autor_atual


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    autor_para_excluir = db.get(Author, author_id)

    if autor_para_excluir is None:
        raise HTTPException(
            status_code=404,
            detail="Autor não encontrado"
        )

    db.delete(autor_para_excluir)
    db.commit()
