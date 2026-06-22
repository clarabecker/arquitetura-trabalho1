from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import time

from database import Base, engine, get_db

app = FastAPI(title="Restaurante Service")

class DBRestaurante(Base):
    __tablename__ = "restaurantes"

    idRestaurante = Column(Integer, primary_key=True, index=True)
    nmRestaurante = Column(String, nullable=False)
    nmEndereco = Column(String, nullable=False)
    nrTelefone = Column(String, nullable=False)
    nrFuncionarios = Column(Integer, nullable=False)


class RestauranteCreate(BaseModel):
    idRestaurante: int
    nmRestaurante: str
    nmEndereco: str
    nrTelefone: int
    nrFuncionarios: int


class RestauranteResponse(BaseModel):
    idRestaurante: int
    nmRestaurante: str
    nmEndereco: str
    nrTelefone: int
    nrFuncionarios: int

    class Config:
        from_attributes = True

@app.on_event("startup")
def startup():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            time.sleep(2)

@app.post(
    "/restaurantes/",
    response_model=RestauranteResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar(rest: RestauranteCreate, db: Session = Depends(get_db)):

    db_restaurante = db.query(DBRestaurante).filter(
        DBRestaurante.idRestaurante == rest.idRestaurante
    ).first()

    if db_restaurante:
        raise HTTPException(status_code=400, detail="ID já existe.")

    novo_restaurante = DBRestaurante(
        idRestaurante=rest.idRestaurante,
        nmRestaurante=rest.nmRestaurante,
        nmEndereco=rest.nmEndereco,
        nrTelefone=rest.nrTelefone,
        nrFuncionarios=rest.nrFuncionarios
    )

    db.add(novo_restaurante)
    db.commit()
    db.refresh(novo_restaurante)

    return novo_restaurante


@app.get("/restaurantes/{id}", response_model=RestauranteResponse)
def obter(id: int, db: Session = Depends(get_db)):

    restaurante = db.query(DBRestaurante).filter(
        DBRestaurante.idRestaurante == id
    ).first()

    if not restaurante:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado.")

    return restaurante