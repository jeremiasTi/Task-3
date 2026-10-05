from fastapi import FastAPI

from app.routers import authors, books

app = FastAPI(title="Biblioteca API", version="1.0.0", description="API de autores e livros")
app.include_router(authors.router, prefix="/api/v1")
app.include_router(books.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check():
    return {"message": "Biblioteca API funcionando"}

