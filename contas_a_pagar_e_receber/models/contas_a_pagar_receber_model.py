from decimal import Decimal
from sqlalchemy import Column, Integer, String, Float

from shared.database import Base


class ContaPagarReceber (Base):
    __tablename__ = 'contas_a_pagar_receber'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Float)
    tipo = Column(String(30))