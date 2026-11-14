"""
Logger central do projeto.

Uso:

from src.logger import obter_logger

log = obter_logger(__name__)

log.info("Processamento iniciado")
log.warning("Arquivo não encontrado")
log.error("Falha ao carregar dados")
"""

import logging
import sys
from pathlib import Path

from src import config


def configurar_logger() -> None:
    """
    Configura logging global do projeto.
    """

    log_dir = config.ROOT_DIR / "logs"
    log_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_file = log_dir / "tech_challenge.log"

    formato = (
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    )

    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                log_file,
                encoding="utf-8",
            ),
        ],
        force=True,
    )


def obter_logger(nome: str) -> logging.Logger:
    """
    Retorna instância configurada de logger.

    Args:
        nome: normalmente __name__

    Returns:
        Logger configurado
    """
    return logging.getLogger(nome)


# Configura automaticamente ao importar
configurar_logger()
