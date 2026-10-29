# Apresentação — Biblioteca API

Roteiro para a apresentação curta (5 a 10 minutos) com demonstração da API pelo
Swagger (`/docs`).

## Antes de começar (checklist)

- [ ] Ambiente virtual ativado e dependências instaladas (`pip install -r requirements.txt`).
- [ ] Banco atualizado com `alembic upgrade head`.
- [ ] Servidor no ar com `uvicorn app.main:app --reload`.
- [ ] Navegador aberto em http://127.0.0.1:8000/docs.
- [ ] Banco sem registros antigos (se necessário, apague `biblioteca.db` e rode a migration de novo).

> Dica: faça uma execução completa do roteiro antes da aula, em outra janela, para
> confirmar que os IDs retornados serão os esperados.

## Divisão do tempo (8 minutos)

| Tempo | Momento | O que mostrar |
|---|---|---|
| 0:00–1:00 | Abertura | Problema, proposta da API e tecnologias. |
| 1:00–2:30 | Modelo e arquitetura | Relacionamento 1:N e camadas do projeto. |
| 2:30–3:30 | Decisões técnicas | FastAPI, Pydantic, SQLAlchemy e Alembic. |
| 3:30–7:00 | Demonstração | Fluxo completo no Swagger, incluindo erros. |
| 7:00–8:00 | Fechamento | Regras, limitações e próximos passos. |

Se a equipe tiver três pessoas, uma sugestão é dividir assim: abertura/modelo,
decisões técnicas e demonstração, fechamento/perguntas.

## Roteiro de slides (opcional)

1. **Capa** — Biblioteca API, Prática 03, integrantes.
2. **Problema e proposta** — organizar autores e livros com integridade.
3. **Modelo de dados** — `Author (1) ──< (N) Book`, com `author_id` como chave estrangeira.
4. **Arquitetura** — cliente → router → schema → model → banco; Alembic versiona a estrutura.
5. **Tecnologias** — FastAPI, Pydantic, SQLAlchemy 2, Alembic, SQLite.
6. **Demonstração** — Swagger ao vivo.
7. **Fechamento** — limitações conscientes e próximos passos.

## Demonstração no Swagger (passo a passo)

Abra http://127.0.0.1:8000/docs. Para cada endpoint, clique em **Try it out**,
cole o corpo JSON e clique em **Execute**.

### 1. Criar um autor — `POST /api/v1/authors`

```json
{
  "name": "Machado de Assis",
  "email": "machado@example.com"
}
```

Resposta esperada: `201 Created`.

```json
{
  "id": 1,
  "name": "Machado de Assis",
  "email": "machado@example.com"
}
```

Fale: o `id` é gerado pelo banco e o schema de resposta garante o formato.

### 2. Criar um livro — `POST /api/v1/books`

```json
{
  "title": "Dom Casmurro",
  "isbn": "9788535910663",
  "published_year": 1899,
  "author_id": 1
}
```

Resposta esperada: `201 Created`.

Fale: antes do `INSERT`, a API verifica se o autor existe (`ensure_author`);
o ISBN e o e-mail têm restrição de unicidade no banco.

### 3. Listar e consultar — `GET /api/v1/books` e `GET /api/v1/books/1`

Mostre a lista com o livro criado e depois a consulta por id. Resposta `200 OK`.

### 4. Livros por autor — `GET /api/v1/books/author/1`

Mostre os livros do autor 1. Fale: essa rota valida o autor antes de consultar,
para diferenciar “autor sem livros” (`200` com lista vazia) de “autor inexistente”
(`404`).

### 5. Erro de duplicidade — `POST /api/v1/books` com o mesmo ISBN

Repita o corpo do passo 2. Resposta esperada: `409 Conflict`.

```json
{
  "detail": "ISBN já cadastrado"
}
```

Fale: o `IntegrityError` do SQLAlchemy é traduzido para HTTP 409, e o `rollback`
deixa a sessão pronta para a próxima operação.

### 6. Erro de autor inexistente — `POST /api/v1/books` com `author_id: 999`

```json
{
  "title": "Livro sem autor",
  "isbn": "9780000000002",
  "published_year": 2020,
  "author_id": 999
}
```

Resposta esperada: `404 Not Found`, com `"Autor não encontrado"`.

### 7. Erro de validação — `POST /api/v1/books` com ano negativo

```json
{
  "title": "Ano inválido",
  "isbn": "9780000000003",
  "published_year": -5,
  "author_id": 1
}
```

Resposta esperada: `422 Unprocessable Entity`, gerada automaticamente pelo
Pydantic antes de chegar ao banco.

### 8. Atualização parcial — `PUT /api/v1/books/1`

```json
{
  "title": "Dom Casmurro (edição revisada)"
}
```

Resposta esperada: `200 OK`, mantendo ISBN, ano e autor. Fale: usamos
`exclude_unset=True` para alterar apenas os campos enviados.

### 9. Exclusão em cascata — `DELETE /api/v1/authors/1`

Resposta esperada: `204 No Content`. Em seguida, execute `GET /api/v1/books` e
mostre a lista vazia. Fale: os livros do autor foram excluídos pelo cascade do
ORM e pelo `ondelete="CASCADE"` da chave estrangeira.

## Falas prontas

- “A API é organizada em camadas: o router recebe a requisição, o schema valida,
  o model representa a tabela e o banco garante as restrições.”
- “O banco não é criado pelo código da aplicação; ele é criado e versionado pelas
  migrations do Alembic.”
- “A validação acontece em duas defesas: o Pydantic valida a entrada e o banco
  impõe `UNIQUE`, `NOT NULL` e a chave estrangeira.”
- “Os erros têm significado HTTP: 404 para recurso inexistente, 409 para conflito
  de unicidade e 422 para dados inválidos.”

## Fechamento

- O projeto entrega CRUD completo de autores e livros, relacionamento 1:N,
  validação de entrada, integridade no banco e documentação automática.
- Limitações conscientes: não há autenticação, paginação nem testes automatizados;
  o `PUT` faz atualização parcial; o SQLite é adequado ao desenvolvimento.
- Próximos passos: testes com pytest, autenticação JWT, paginação/filtros e
  migração para PostgreSQL apenas trocando a `DATABASE_URL`.

## Plano B

Se o ambiente falhar durante a demonstração:

1. Mostre o arquivo `alembic/versions/0001_create_authors_and_books.py` e explique
   como o banco é criado.
2. Mostre os models e schemas para comprovar as validações e o relacionamento.
3. Abra o `Guia_Biblioteca_API.pdf`, que contém o mesmo fluxo e os exemplos.
4. Se possível, rode os mesmos passos com `curl` ou Postman.

## Perguntas prováveis

As respostas estão na seção 11 do `Guia_Biblioteca_API.pdf`, incluindo: por que
FastAPI, diferença entre model e schema, papel do Alembic, função do
`Depends(get_db)`, cascade, status 409/422, async, troca para PostgreSQL e
limitações do projeto.
