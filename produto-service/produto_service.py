from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float

from database import Base, engine, get_db

# Cria a tabela de produtos se não existir
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Produto Service")

class DBProduto(Base):
    __tablename__ = "produtos"
    
    idProduto = Column(Integer, primary_key=True, index=True)
    nmProduto = Column(String, nullable=False)
    dsProduto = Column(String, nullable=False)
    vlProduto = Column(Float, nullable=False)
    dtValidade = Column(String, nullable=False)

class ProdutoSchema(BaseModel):
    idProduto: int
    nmProduto: str
    dsProduto: str
    vlProduto: float
    dtValidade: str

    class Config:
        from_attributes = True

# --- ROTAS ---

@app.post("/produtos/", response_model=ProdutoSchema, status_code=status.HTTP_201_CREATED)
def cadastrar(prod: ProdutoSchema, db: Session = Depends(get_db)):
    db_produto = db.query(DBProduto).filter(DBProduto.idProduto == prod.idProduto).first()
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

@app.get("/produtos/{id}", response_model=ProdutoSchema)
def obter(id: int, db: Session = Depends(get_db)):
    produto = db.query(DBProduto).filter(DBProduto.idProduto == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto