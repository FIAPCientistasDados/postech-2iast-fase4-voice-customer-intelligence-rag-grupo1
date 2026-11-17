from src import config
from src.logger import obter_logger

log = obter_logger(__name__)


def validar_dataset():

    faltando = []

    for arquivo in config.ARQUIVOS_OLIST:

        caminho = (
            config.DADOS_BRUTOS / arquivo
        )

        if not caminho.exists():

            faltando.append(
                arquivo
            )

    if faltando:

        raise FileNotFoundError(
            f"Arquivos ausentes: {faltando}"
        )

    log.info(
        "Dataset validado com sucesso."
    )


if __name__ == "__main__":

    validar_dataset()
