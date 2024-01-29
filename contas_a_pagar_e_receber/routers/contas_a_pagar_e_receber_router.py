from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import ContaPagarReceber
from contas_a_pagar_e_receber.routers.fornecedor_cliente_router import FornecedorClienteResponse

from shared.dependecies import get_db
from shared.exceptions import NotFoundExecption

router = APIRouter(prefix="/contas-a-pagar-e-receber")

class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str #PAGAR, RECEBER
    fornecedor: FornecedorClienteResponse | None = None
    class Config:
        from_attributes = True

class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'    

class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum
    fornecedor_cliente_id: int | None = None

@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas(db:Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()

@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest, db:Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(**conta.model_dump())
    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)
    return contas_a_pagar_e_receber

@router.put("/{id_conta_a_pagar_e_receber}", response_model=ContaPagarReceberResponse, status_code=200)
def atualizar_conta(
        id_conta_a_pagar_e_receber: int,
        conta_request: ContaPagarReceberRequest, 
        db:Session = Depends(get_db)
    ) -> ContaPagarReceberResponse:
    
    conta_a_pagar_do_banco: ContaPagarReceber = busca_conta_pelo_id(id_conta_a_pagar_e_receber=id_conta_a_pagar_e_receber, db=db)
    if not conta_a_pagar_do_banco:
        raise NotFoundExecption("Conta a Pagar e Receber")
    conta_a_pagar_do_banco.tipo = conta_request.tipo
    conta_a_pagar_do_banco.valor = conta_request.valor
    conta_a_pagar_do_banco.descricao = conta_request.descricao
    
    db.add(conta_a_pagar_do_banco)
    db.commit()
    db.refresh(conta_a_pagar_do_banco)
    return conta_a_pagar_do_banco

@router.delete("/{id_conta_a_pagar_e_receber}", status_code=204)
def deletar_conta(
        id_conta_a_pagar_e_receber: int,
        db:Session = Depends(get_db)
    ):
    conta_a_pagar_do_banco: ContaPagarReceber = busca_conta_pelo_id(id_conta_a_pagar_e_receber=id_conta_a_pagar_e_receber, db=db)
    if not conta_a_pagar_do_banco:
        raise NotFoundExecption("Conta a Pagar e Receber")
    db.delete(conta_a_pagar_do_banco)
    db.commit()
    
@router.get("/{id_conta_a_pagar_e_receber}", response_model=ContaPagarReceberResponse, status_code=200)
def listar_conta(
        id_conta_a_pagar_e_receber: int,
        db:Session = Depends(get_db)
    ) -> ContaPagarReceberResponse:
    
    conta_a_pagar_do_banco: ContaPagarReceber = busca_conta_pelo_id(id_conta_a_pagar_e_receber=id_conta_a_pagar_e_receber, db=db)
    if not conta_a_pagar_do_banco:
        raise NotFoundExecption("Conta a Pagar e Receber")
    return conta_a_pagar_do_banco

def busca_conta_pelo_id( 
        id_conta_a_pagar_e_receber: int,
        db:Session) -> ContaPagarReceber: 
    return db.query(ContaPagarReceber).get(id_conta_a_pagar_e_receber)