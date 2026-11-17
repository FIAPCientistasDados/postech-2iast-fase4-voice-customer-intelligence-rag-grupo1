"""
Baixa automaticamente o dataset Olist
e copia os CSVs necessários para data/raw.

Uso:

python -m src.ingestion.baixar_dados
"""

from pathlib import Path
import shutil

import kagglehub

from src import config
from src.logger import obter_logger

log = obter_logger(__name__)


def baixar() -> Path:
    """
    Baixa o dataset Olist
    e copia os arquivos necessários.

    Returns
    -------
    Path
        Diretório data/raw
    """

    destino = config.DADOS_BRUTOS

    faltando = [
        arquivo
        for arquivo in config.ARQUIVOS_OLIST
        if not (destino / arquivo).exists()
    ]

    if not faltando:

        log.info(
            "Todos os arquivos já estão disponíveis."
        )

        return destino

    log.info(
        "Iniciando download do dataset Olist..."
    )

    try:

        origem = Path(
            kagglehub.dataset_download(
                config.KAGGLE_DATASET
            )
        )

        log.info(
            "Dataset baixado para %s",
            origem,
        )

    except Exception as erro:

        log.exception(
            "Falha ao baixar dataset."
        )

        raise erro

    for arquivo in faltando:

        origem_arquivo = origem / arquivo
        destino_arquivo = destino / arquivo

        if not origem_arquivo.exists():

            log.error(
                "Arquivo ausente no dataset: %s",
                arquivo,
            )

            raise FileNotFoundError(
                f"Arquivo não encontrado: {arquivo}"
            )

        shutil.copy2(
            origem_arquivo,
            destino_arquivo,
        )

        log.info(
            "Arquivo copiado: %s",
            arquivo,
        )

    log.info(
        "Download finalizado com sucesso."
    )

    return destino


def validar_base() -> bool:
    """
    Verifica se todos os arquivos existem.
    """

    faltando = []

    for arquivo in config.ARQUIVOS_OLIST:

        if not (
            config.DADOS_BRUTOS / arquivo
        ).exists():

            faltando.append(
                arquivo
            )

    if faltando:

        log.warning(
            "Arquivos faltando: %s",
            faltando,
        )

        return False

    log.info(
        "Base validada com sucesso."
    )

    return True


if __name__ == "__main__":

    baixar()
    validar_base()

