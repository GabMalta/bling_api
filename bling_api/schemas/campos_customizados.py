from typing import Optional
from pydantic import BaseModel


class CampoCustomizado(BaseModel):
    idCampoCustomizado: int
    idVinculo: int
    valor: Optional[str] = ""
    item: Optional[str] = ""


def campos_customizados_padrao():
    return [
        CampoCustomizado(
            idCampoCustomizado=2668618,  # MarcaShopee
            idVinculo=752799787,
            valor="227760129",
            item="Legítima Têxtil",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668619,  # Pais de Origem
            idVinculo=752799788,
            valor="227760240",
            item="China",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668624,  # Quantidade
            idVinculo=752799790,
            valor="1",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668654,  # Modelo ML
            idVinculo=752799792,
            valor="Tecido",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668655,  # Material ML
            idVinculo=752799793,
            valor="Textil",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668658,  # Composicao ML
            idVinculo=752799794,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668659,  # largura(m) ML
            idVinculo=752799795,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668660,  # comprimento(m) ML
            idVinculo=752799796,
            valor="1",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=2668665,  # Codigo Universal do Produto
            idVinculo=752799798,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3480772,  # Produto Personalizado
            idVinculo=1004684146,
            valor="315789973",
            item="Não",
        ),
        CampoCustomizado(
            idCampoCustomizado=3481925,  # tamanho pacote SHOPEE
            idVinculo=1042821908,
            valor="1",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3488587,  # Tipo de Estilo
            idVinculo=0,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3627028,  # Marca ML
            idVinculo=1042821909,
            valor="Legítima Têxtil",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3627057,  # Tipo Produto ML
            idVinculo=1042821910,
            valor="333803718",
            item="Rolo",
        ),
        CampoCustomizado(
            idCampoCustomizado=3676328,  # Cor Principal ML
            idVinculo=1042821911,
            valor="337350351",
            item="Multicolorido",
        ),
        CampoCustomizado(
            idCampoCustomizado=3676332,  # Usos Recomendados ML
            idVinculo=1042821912,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3676335,  # Peso ML
            idVinculo=1042821913,
            valor="",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3676337,  # Adequado Maquina de Lavar
            idVinculo=1042821914,
            valor="true",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3676338,  # Adequado Secadora de Roupas
            idVinculo=1042821915,
            valor="true",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3676340,  # Adequado Passar Ferro
            idVinculo=1042821916,
            valor="true",
            item="",
        ),
        CampoCustomizado(
            idCampoCustomizado=3676440,  # Dimensões do Produto (A x L x C), sem a caixa
            idVinculo=1043070256,
            valor="",
            item="",
        ),
    ]
