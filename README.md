# Biblioteca API

API REST para gerenciamento de autores e livros, desenvolvida para a Prática 03.

## Modelo de negócio

Uma biblioteca possui **autores** e **livros**. Um autor pode escrever vários livros,
mas cada livro pertence a um único autor.

```text
Author (1) ───────────< (N) Book
  id                    id
  name                  title
  email                 isbn
                        published_year
                        author_id (FK)
```

O relacionamento é implementado com `ForeignKey("authors.id")` e `relationship()`
do SQLAlchemy nos dois modelos.

## Tecnologias

- Python 3.10+
- FastAPI e Uvicorn
- SQLAlchemy 2 (ORM)
- Alembic (migrações)
- Pydantic 2 (validação)
- SQLite por padrão

## Instalação e execução

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env            # opcional
alembic upgrade head
uvicorn app.main:app --reload
```

Abra http://127.0.0.1:8000/docs para testar via Swagger.

O banco é criado exclusivamente pela migration do Alembic. Para gerar uma nova
migration depois de alterar os modelos:

```bash
alembic revision --autogenerate -m "descricao da alteracao"
alembic upgrade head
```

## Endpoints

### Autores

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/authors` | Criar autor |
| GET | `/api/v1/authors` | Listar autores |
| GET | `/api/v1/authors/{author_id}` | Consultar autor |
| PUT | `/api/v1/authors/{author_id}` | Atualizar autor |
| DELETE | `/api/v1/authors/{author_id}` | Excluir autor |

### Livros

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/books` | Criar livro; valida se o autor existe |
| GET | `/api/v1/books` | Listar livros |
| GET | `/api/v1/books/{book_id}` | Consultar livro |
| PUT | `/api/v1/books/{book_id}` | Atualizar livro |
| DELETE | `/api/v1/books/{book_id}` | Excluir livro |

Respostas de criação usam `201`, recursos inexistentes usam `404` e erros de
validação de entrada retornam `422` automaticamente pelo FastAPI.

## Estrutura

```text
app/
├── core/          # configurações e banco
├── models/        # entidades ORM
├── schemas/       # contratos Pydantic (Create, Update, Response)
├── routers/       # endpoints HTTP
└── main.py
alembic/versions/  # migrations versionadas
```

