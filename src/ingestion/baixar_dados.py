"""
Download do dataset Olist.

Responsabilidades:
- Verificar se os arquivos já existem em data/raw
- Baixar automaticamente o dataset do Kaggle
- Copiar apenas os arquivos necessários
- Registrar todas as etapas em log

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
    Baixa o dataset Olist e copia os arquivos
    necessários para o diretório data/raw.

    Returns
    -------
    Path
        Caminho da pasta contendo os dados brutos.
    """

    destino = config.DADOS_BRUTOS

    destino.mkdir(
        parents=True,
        exist_ok=True,
    )

    faltando = [
        arquivo
        for arquivo in config.ARQUIVOS_OLIST
        if not (destino / arquivo).exists()
    ]

    if not faltando:
        log.info(
            "Base já disponível em %s",
            destino,
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
        log.error(
            "Falha ao baixar dataset: %s",
            erro,
        )
        raise

    for arquivo in faltando:

        origem_arquivo = origem / arquivo
        destino_arquivo = destino / arquivo

        if not origem_arquivo.exists():

            log.error(
                "Arquivo não encontrado no dataset: %s",
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
        "Download concluído com sucesso."
    )

    return destino


def validar_base() -> bool:
    """
    Verifica se todos os arquivos
    necessários estão disponíveis.

    Returns
    -------
    bool
    """

    arquivos_faltantes = [
        arquivo
        for arquivo in config.ARQUIVOS_OLIST
        if not (
            config.DADOS_BRUTOS / arquivo
        ).exists()
    ]

    if arquivos_faltantes:

        log.warning(
            "Arquivos ausentes: %s",
            arquivos_faltantes,
        )

        return False

    log.info(
        "Todos os arquivos foram encontrados."
    )

    return True


if __name__ == "__main__":

    try:

        baixar()

        if validar_base():

            log.info(
                "Dataset pronto para uso."
            )

    except Exception as erro:

        log.exception(
            "Erro durante ingestão: %s",
            erro,
        )

        raise
