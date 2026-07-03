from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import engine, get_db

# Cria as tabelas no banco (caso ainda não existam)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Usuários",
    description="CRUD da tabela usuarios usando FastAPI + PostgreSQL",
    version="1.0.0",
)


@app.get("/")
def raiz():
    return {"mensagem": "API de Usuários rodando! Acesse /docs para testar."}


# ---------- CREATE ----------
@app.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioBase, db: Session = Depends(get_db)):
    if crud.get_usuario_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    return crud.criar_usuario(db, usuario)


# ---------- READ (lista) ----------
@app.get("/usuarios", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_usuarios(db, skip, limit)


# ---------- READ (por id) ----------
@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_usuario


# ---------- UPDATE ----------
@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud.atualizar_usuario(db, usuario_id, dados)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_usuario


# ---------- DELETE ----------
@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.deletar_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return None