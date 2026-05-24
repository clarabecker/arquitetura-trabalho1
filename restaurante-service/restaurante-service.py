from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Restaurante Service")

class Restaurante(BaseModel):
    idRestaurante: int
    nmRestaurante: str
    nmEndereco: str
    nrTelefone: int
    nrFuncionarios: int

DB: List[Restaurante] = [
    Restaurante(idRestaurante=1, nmRestaurante="Burguer King UDESC", nmEndereco="Rua Central, 123", nrTelefone=33570000, nrFuncionarios=12)
]

@app.post("/restaurantes/", status_code=status.HTTP_201_CREATED)
def cadastrar(rest: Restaurante):
    if any(r.idRestaurante == rest.idRestaurante for r in DB):
        raise HTTPException(status_code=400, detail="ID já existe.")
    DB.append(rest)
    return rest

@app.get("/restaurantes/{id}")
def obter(id: int):
    for r in DB:
        if r.idRestaurante == id:
            return r
    raise HTTPException(status_code=404, detail="Restaurante não encontrado.")