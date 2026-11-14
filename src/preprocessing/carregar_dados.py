import pandas as pd

from src import config
from src.logger import obter_logger

log = obter_logger(__name__)


def carregar_dados():

    log.info("Carregando reviews")

    reviews = pd.read_csv(
        config.ARQUIVO_REVIEWS
    )

    log.info("Carregando pedidos")

    orders = pd.read_csv(
        config.ARQUIVO_ORDERS
    )

    log.info("Carregando produtos")

    products = pd.read_csv(
        config.ARQUIVO_PRODUCTS
    )

    return reviews, orders, products
