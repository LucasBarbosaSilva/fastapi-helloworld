from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.fornecedor_cliente_model import FornecedorCliente

from shared.dependecies import get_db
from shared.exceptions import NotFoundExecption
endpoint = "/fornecedor-cliente"
router = APIRouter(prefix=endpoint)

class FornecedorClienteResponse(BaseModel):
    id: int = Field(index=True)
    nome: str = Field(index=True)
    
    class Config:
        from_attributes = True

class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=250)

@router.get("", response_model=List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db:Session = Depends(get_db)) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).all()

@router.post("", response_model=FornecedorClienteResponse, status_code=201)
def criar_fornecedor_cliente(fornecedor_cliente: FornecedorClienteRequest, db:Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor_cliente = FornecedorCliente(**fornecedor_cliente.model_dump())
    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)
    return fornecedor_cliente

@router.put("/{id_fornecedor_cliente}", response_model=FornecedorClienteResponse, status_code=200)
def atualizar_fornecedor_cliente(
        id_fornecedor_cliente: int,
        fornecedor_cliente_request: FornecedorClienteRequest, 
        db:Session = Depends(get_db)
    ) -> FornecedorClienteResponse:
    
    fornecedor_cliente_do_banco: FornecedorCliente = busca_fornecedor_cliente_pelo_id(id_fornecedor_cliente=id_fornecedor_cliente, db=db)
    if not fornecedor_cliente_do_banco:
        raise NotFoundExecption("Fornecedor Cliente")
    fornecedor_cliente_do_banco.nome = fornecedor_cliente_request.nome
    
    db.add(fornecedor_cliente_do_banco)
    db.commit()
    db.refresh(fornecedor_cliente_do_banco)
    return fornecedor_cliente_do_banco

@router.delete("/{id_fornecedor_cliente}", status_code=204)
def deletar_fornecedor_cliente(
        id_fornecedor_cliente: int,
        db:Session = Depends(get_db)
    ):
    fornecedor_cliente_do_banco: FornecedorCliente = busca_fornecedor_cliente_pelo_id(id_fornecedor_cliente=id_fornecedor_cliente, db=db)
    if not fornecedor_cliente_do_banco:
        raise NotFoundExecption("Fornecedor Cliente")
    db.delete(fornecedor_cliente_do_banco)
    db.commit()
    
@router.get("/{id_fornecedor_cliente}", response_model=FornecedorClienteResponse, status_code=200)
def listar_fornecedor_cliente(
        id_fornecedor_cliente: int,
        db:Session = Depends(get_db)
    ) -> FornecedorClienteResponse:
    
    fornecedor_cliente_do_banco: FornecedorCliente = busca_fornecedor_cliente_pelo_id(id_fornecedor_cliente=id_fornecedor_cliente, db=db)
    if not fornecedor_cliente_do_banco:
        raise NotFoundExecption("Fornecedor Cliente")
    return fornecedor_cliente_do_banco

def busca_fornecedor_cliente_pelo_id( 
        id_fornecedor_cliente: int,
        db:Session) -> FornecedorCliente: 
    return db.query(FornecedorCliente).get(id_fornecedor_cliente)