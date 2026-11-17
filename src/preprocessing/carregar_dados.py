"""
Carregamento centralizado dos datasets Olist.

Responsabilidades:
- Ler todos os CSVs necessários
- Validar existência dos arquivos
- Exibir informações de carregamento
- Retornar DataFrames organizados

Uso:

from src.preprocessing.carregar_dados import carregar_dados

dados = carregar_dados()

reviews = dados["reviews"]
orders = dados["orders"]
products = dados["products"]
"""

from typing import Dict

import pandas as pd

from src import config
from src.logger import obter_logger

log = obter_logger(__name__)


def _validar_arquivo(caminho):
    """
    Verifica se o arquivo existe.

    Parameters
    ----------
    caminho : Path

    Raises
    ------
    FileNotFoundError
    """
    if not caminho.exists():

        log.error(
            "Arquivo não encontrado: %s",
            caminho,
        )

        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        )


def carregar_dados() -> Dict[str, pd.DataFrame]:
    """
    Carrega todos os datasets Olist utilizados no projeto.

    Returns
    -------
    Dict[str, pd.DataFrame]
    """

    log.info(
        "Iniciando carregamento dos datasets..."
    )

    arquivos = {
        "customers": config.ARQUIVO_CUSTOMERS,
        "order_items": config.ARQUIVO_ORDER_ITEMS,
        "reviews": config.ARQUIVO_REVIEWS,
        "orders": config.ARQUIVO_ORDERS,
        "products": config.ARQUIVO_PRODUCTS,
        "categories": config.ARQUIVO_CATEGORY_TRANSLATION,
    }

    for nome, caminho in arquivos.items():

        _validar_arquivo(caminho)

        log.info(
            "Arquivo validado: %s",
            caminho.name,
        )

    try:

        customers = pd.read_csv(
            config.ARQUIVO_CUSTOMERS
        )

        order_items = pd.read_csv(
            config.ARQUIVO_ORDER_ITEMS
        )

        reviews = pd.read_csv(
            config.ARQUIVO_REVIEWS
        )

        orders = pd.read_csv(
            config.ARQUIVO_ORDERS
        )

        products = pd.read_csv(
            config.ARQUIVO_PRODUCTS
        )

        categories = pd.read_csv(
            config.ARQUIVO_CATEGORY_TRANSLATION
        )

    except Exception as erro:

        log.exception(
            "Erro ao carregar os CSVs."
        )

        raise erro

    log.info(
        "Customers carregado: %s registros",
        len(customers),
    )

    log.info(
        "Order Items carregado: %s registros",
        len(order_items),
    )

    log.info(
        "Reviews carregado: %s registros",
        len(reviews),
    )

    log.info(
        "Orders carregado: %s registros",
        len(orders),
    )

    log.info(
        "Products carregado: %s registros",
        len(products),
    )

    log.info(
        "Categories carregado: %s registros",
        len(categories),
    )

    log.info(
        "Todos os datasets carregados com sucesso."
    )

    return {
        "customers": customers,
        "order_items": order_items,
        "reviews": reviews,
        "orders": orders,
        "products": products,
        "categories": categories,
    }


def exibir_resumo(dados):
    """
    Exibe resumo dos DataFrames carregados.

    Parameters
    ----------
    dados : Dict[str, pd.DataFrame]
    """

    print("\n=== RESUMO DOS DATASETS ===\n")

    for nome, dataframe in dados.items():

        print(
            f"{nome:<15}"
            f" -> "
            f"{len(dataframe):,} linhas | "
            f"{len(dataframe.columns)} colunas"
        )


if __name__ == "__main__":

    dados = carregar_dados()

    exibir_resumo(dados)

