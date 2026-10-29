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

### Regras de negócio

- Todo livro pertence a exatamente um autor e só pode ser criado se o autor existir.
- O e-mail de um autor e o ISBN de um livro não podem se repetir.
- Ao excluir um autor, os livros dele são excluídos em cascata.
- O nome do autor deve ter entre 2 e 120 caracteres; o título, entre 1 e 200.
- O ISBN deve ter entre 10 e 20 caracteres e o ano de publicação, entre 0 e 2100.

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
source .venv/bin/activate       # Windows: .venv\Scripts\activate
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
| GET | `/api/v1/books/author/{author_id}` | Listar os livros de um autor |

Respostas de criação usam `201`, exclusões usam `204`, recursos inexistentes usam
`404`, conflitos de unicidade (e-mail ou ISBN repetido) usam `409` e erros de
validação de entrada retornam `422` automaticamente pelo FastAPI.

## Apresentação e demonstração

Roteiro completo da apresentação de 5 a 10 minutos em
[APRESENTACAO.md](APRESENTACAO.md), incluindo divisão de falas, sequência de
demonstração no Swagger e plano B. Resumo:

1. Contexto: uma biblioteca precisa organizar autores e livros e manter a integridade entre eles.
2. Modelo e arquitetura: relacionamento 1:N, camadas `router → schema → model → banco` e migrations com Alembic.
3. Demonstração em http://127.0.0.1:8000/docs: criar autor, criar livro, listar, consultar por autor e provocar os erros 404, 409 e 422.
4. Fechamento: decisões técnicas, limitações conscientes e próximos passos.

## Material de apoio

O guia de estudo completo (PDF) reúne a explicação de cada arquivo, o fluxo de uma
requisição, glossário e perguntas prováveis do professor. Ele é distribuído
separadamente pela equipe e não é versionado no repositório.

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

