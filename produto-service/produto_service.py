from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
import time 
from sqlalchemy.exc import OperationalError

from database import Base, engine, get_db

app = FastAPI(title="Produto Service")


class DBProduto(Base):
    __tablename__ = "produtos"

    idProduto = Column(Integer, primary_key=True, index=True)
    nmProduto = Column(String, nullable=False)
    dsProduto = Column(String, nullable=False)
    vlProduto = Column(Float, nullable=False)
    dtValidade = Column(String, nullable=False)

class ProdutoCreate(BaseModel):
    idProduto: int
    nmProduto: str
    dsProduto: str
    vlProduto: float
    dtValidade: str


class ProdutoResponse(BaseModel):
    idProduto: int
    nmProduto: str
    dsProduto: str
    vlProduto: float
    dtValidade: str

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
    "/produtos/",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar(prod: ProdutoCreate, db: Session = Depends(get_db)):

    db_produto = db.query(DBProduto).filter(
        DBProduto.idProduto == prod.idProduto
    ).first()

    if db_produto:
        raise HTTPException(status_code=400, detail="ID já existe.")

    novo_produto = DBProduto(
        idProduto=prod.idProduto,
        nmProduto=prod.nmProduto,
        dsProduto=prod.dsProduto,
        vlProduto=prod.vlProduto,
        dtValidade=prod.dtValidade
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@app.get("/produtos/{id}", response_model=ProdutoResponse)
def obter(id: int, db: Session = Depends(get_db)):

    produto = db.query(DBProduto).filter(
        DBProduto.idProduto == id
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return produto