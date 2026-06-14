from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

# Importando nossa conexão de banco
from database import Base, engine, get_db

# 1. Cria as tabelas no banco de dados se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cliente Service")

# 2. Modelo do Banco de Dados (SQLAlchemy)
class DBCliente(Base):
    __tablename__ = "clientes"
    
    idCliente = Column(Integer, primary_key=True, index=True)
    nmCliente = Column(String, nullable=False)
    nrTelefone = Column(String, nullable=False)
    strEmail = Column(String, nullable=False)

# 3. Esquema de Validação (Pydantic - o que entra e sai da API)
class ClienteSchema(BaseModel):
    idCliente: int
    nmCliente: str
    nrTelefone: str
    strEmail: str

    class Config:
        from_attributes = True # Permite que o Pydantic leia dados do SQLAlchemy

# --- ROTAS ---

@app.post("/clientes/", response_model=ClienteSchema, status_code=status.HTTP_201_CREATED)
def cadastrar(cli: ClienteSchema, db: Session = Depends(get_db)):
    # Verifica se o ID já existe no banco
    db_cliente = db.query(DBCliente).filter(DBCliente.idCliente == cli.idCliente).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="ID já existe.")
    
    # Converte o esquema Pydantic para o modelo SQLAlchemy
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

@app.get("/clientes/{id}", response_model=ClienteSchema)
def obter(id: int, db: Session = Depends(get_db)):
    cliente = db.query(DBCliente).filter(DBCliente.idCliente == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente