from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TiposProdutos(str, Enum):
    Todos = "T"
    Produtos = "P"
    Servicos = "S"
    Composicoes = "E"
    ProdutosSimples = "PS"
    ComVariacoes = "C"
    Variacoes = "V"


class GetProductsParamsSchema(BaseModel):
    pagina: int = Field(default=1, ge=1)
    limite: int = Field(default=100, ge=1)
    criterio: Optional[int] = Field(default=1, ge=1)
    tipo: Optional[TiposProdutos] = Field(default=TiposProdutos.Todos)
    idComponente: Optional[int] = None

    dataInclusaoInicial: Optional[datetime] = None
    dataInclusaoFinal: Optional[datetime] = None
    dataAlteracaoInicial: Optional[datetime] = None
    dataAlteracaoFinal: Optional[datetime] = None

    idCategoria: Optional[int] = None
    idLoja: Optional[int] = None
    nome: Optional[str] = None

    idsProdutos: Optional[List[int]] = Field(default=None, alias="idsProdutos[]")
    codigos: Optional[List[str]] = Field(default=None, alias="codigos[]")

    filtroSaldoEstoque: Optional[int] = None
    filtroSaldoEstoqueDeposito: Optional[int] = None

    class Config:
        # Permite que Pydantic aceite strings de datas no formato usado pela querystring
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }
        populate_by_name = True
