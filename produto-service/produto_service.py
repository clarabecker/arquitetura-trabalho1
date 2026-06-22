from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

from database import Base, engine, get_db

app = FastAPI(title="Produto Service")


# -----------------------------
# MODEL (SQLAlchemy)
# -----------------------------
class DBProduto(Base):
    __tablename__ = "produtos"

    idProduto = Column(Integer, primary_key=True, index=True)
    nmProduto = Column(String, nullable=False)
    dsProduto = Column(String, nullable=False)
    vlProduto = Column(Float, nullable=False)
    dtValidade = Column(String, nullable=False)


# -----------------------------
# SCHEMA (Pydantic)
# -----------------------------
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


# -----------------------------
# STARTUP (CRIA TABELAS)
# -----------------------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# -----------------------------
# ROTAS
# -----------------------------
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