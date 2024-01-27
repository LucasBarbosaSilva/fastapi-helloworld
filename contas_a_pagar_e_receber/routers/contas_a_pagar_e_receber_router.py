from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.models.contas_a_pagar_receber_model import ContaPagarReceber

from shared.dependecies import get_db

router = APIRouter(prefix="/contas-a-pagar-e-receber")

class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str #PAGAR, RECEBER
    
    class Config:
        from_attributes = True

class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'    

class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum

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
    
    conta_a_pagar_do_banco: ContaPagarReceber = db.query(ContaPagarReceber).get(id_conta_a_pagar_e_receber)
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
    conta = db.query(ContaPagarReceber).get(id_conta_a_pagar_e_receber)
    db.delete(conta)
    db.commit()
    
@router.get("/{id_conta_a_pagar_e_receber}", response_model=ContaPagarReceberResponse, status_code=200)
def listar_conta(
        id_conta_a_pagar_e_receber: int,
        db:Session = Depends(get_db)
    ) -> ContaPagarReceberResponse:
    
    conta_a_pagar_do_banco: ContaPagarReceber = db.query(ContaPagarReceber).get(id_conta_a_pagar_e_receber)
    return conta_a_pagar_do_banco