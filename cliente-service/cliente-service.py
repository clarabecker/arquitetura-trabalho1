from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Cliente Service")

class Cliente(BaseModel):
    idCliente: int
    nmCliente: str
    nrTelefone: str
    strEmail: str

DB: List[Cliente] = [
    Cliente(idCliente=1, nmCliente="Clara Becker", nrTelefone="4799999999", strEmail="clara@udesc.br")
]

@app.post("/clientes/", status_code=status.HTTP_201_CREATED)
def cadastrar(cli: Cliente):
    if any(c.idCliente == cli.idCliente for c in DB):
        raise HTTPException(status_code=400, detail="ID já existe.")
    DB.append(cli)
    return cli

@app.get("/clientes/{id}")
def obter(id: int):
    for c in DB:
        if c.idCliente == id:
            return c
    raise HTTPException(status_code=404, detail="Cliente não encontrado.")