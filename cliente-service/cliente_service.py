from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from database import Base, engine, get_db

app = FastAPI(title="Cliente Service")

class DBCliente(Base):
    __tablename__ = "clientes"

    idCliente = Column(Integer, primary_key=True, index=True)
    nmCliente = Column(String, nullable=False)
    nrTelefone = Column(String, nullable=False)
    strEmail = Column(String, nullable=False)


class ClienteCreate(BaseModel):
    idCliente: int
    nmCliente: str
    nrTelefone: str
    strEmail: str


class ClienteResponse(BaseModel):
    idCliente: int
    nmCliente: str
    nrTelefone: str
    strEmail: str

    class Config:
        from_attributes = True


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.post("/clientes/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def cadastrar(cli: ClienteCreate, db: Session = Depends(get_db)):

    # verifica duplicidade
    db_cliente = db.query(DBCliente).filter(
        DBCliente.idCliente == cli.idCliente
    ).first()

    if db_cliente:
        raise HTTPException(status_code=400, detail="ID já existe.")

    novo_cliente = DBCliente(
        idCliente=cli.idCliente,
        nmCliente=cli.nmCliente,
        nrTelefone=cli.nrTelefone,
        strEmail=cli.strEmail
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


@app.get("/clientes/{id}", response_model=ClienteResponse)
def obter(id: int, db: Session = Depends(get_db)):

    cliente = db.query(DBCliente).filter(
        DBCliente.idCliente == id
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    return cliente