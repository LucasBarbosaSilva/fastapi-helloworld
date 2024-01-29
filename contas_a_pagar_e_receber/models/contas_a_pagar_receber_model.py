from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from shared.database import Base


class ContaPagarReceber (Base):
    __tablename__ = 'contas_a_pagar_receber'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30))
    valor = Column(Float)
    tipo = Column(String(30))
    
    fornecedor_cliente_id = Column(Integer, ForeignKey("fornecedor_cliente.id"))
    fornecedor_cliente = relationship("FornecedorCliente")