from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Produto Service")

class Produto(BaseModel):
    idProduto: int
    nmProduto: str
    dsProduto: str
    vlProduto: float
    dtValidade: str

DB: List[Produto] = [
    # Dados mockup para teste inicial
    Produto(idProduto=1, nmProduto="Hambúrguer", dsProduto="Artesanal", vlProduto=35.00, dtValidade="10/12/2026")
]

@app.post("/produtos/", status_code=status.HTTP_201_CREATED)
def cadastrar(prod: Produto):
    if any(p.idProduto == prod.idProduto for p in DB):
        raise HTTPException(status_code=400, detail="ID já existe.")
    DB.append(prod)
    return prod

@app.get("/produtos/{id}")
def obter(id: int):
    for p in DB:
        if p.idProduto == id:
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado.")