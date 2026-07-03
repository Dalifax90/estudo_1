from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def listar_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()


def criar_usuario(db: Session, usuario: schemas.UsuarioBase):
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
       
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def atualizar_usuario(db: Session, usuario_id: int, dados: schemas.UsuarioUpdate):
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        return None

    dados_dict = dados.model_dump(exclude_unset=True)

    for campo, valor in dados_dict.items():
        setattr(db_usuario, campo, valor)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def deletar_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        return None
    db.delete(db_usuario)
    db.commit()
    return db_usuario