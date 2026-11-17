"""
Preparação da base de conhecimento para o RAG.

Responsabilidades:
- Carregar datasets
- Validar estrutura dos dados
- Validar joins
- Tratar valores ausentes
- Limpar textos
- Enriquecer avaliações com metadados
- Criar documentos para RAG
- Gerar estatísticas
- Salvar dataset processado

Uso:

python -m src.preprocessing.preparar_reviews
"""

import pandas as pd

from src import config
from src.logger import obter_logger
from src.preprocessing.carregar_dados import carregar_dados

log = obter_logger(__name__)


COLUNAS_OBRIGATORIAS = {
    "reviews": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_message",
    ],
    "orders": [
        "order_id",
        "order_purchase_timestamp",
    ],
    "order_items": [
        "order_id",
        "product_id",
    ],
    "products": [
        "product_id",
        "product_category_name",
    ],
    "categories": [
        "product_category_name",
        "product_category_name_english",
    ],
}


def validar_colunas(datasets):

    print("\n=== VALIDAÇÃO DE COLUNAS ===\n")

    for nome, colunas in COLUNAS_OBRIGATORIAS.items():

        faltantes = [
            coluna
            for coluna in colunas
            if coluna not in datasets[nome].columns
        ]

        if faltantes:

            raise ValueError(
                f"{nome}: colunas ausentes "
                f"{faltantes}"
            )

        print(f"{nome:<12} OK")


def validar_joins(
    reviews,
    orders,
    order_items,
    products,
):

    print("\n=== VALIDAÇÃO DOS JOINS ===\n")

    reviews_sem_order = (
        ~reviews["order_id"]
        .isin(orders["order_id"])
    ).sum()

    itens_sem_produto = (
        ~order_items["product_id"]
        .isin(products["product_id"])
    ).sum()

    print(
        f"Reviews sem pedido : "
        f"{reviews_sem_order:,}"
    )

    print(
        f"Itens sem produto  : "
        f"{itens_sem_produto:,}"
    )

    if reviews_sem_order > 0:
        raise ValueError(
            "Existem reviews sem pedidos."
        )

    if itens_sem_produto > 0:
        raise ValueError(
            "Existem produtos órfãos."
        )


def limpar_reviews(
    reviews: pd.DataFrame,
) -> pd.DataFrame:

    total_inicial = len(reviews)

    sem_texto = (
        reviews[
            "review_comment_message"
        ]
        .isna()
        .sum()
    )

    reviews = reviews.dropna(
        subset=[
            "review_comment_message"
        ]
    )

    reviews[
        "review_comment_message"
    ] = (
        reviews[
            "review_comment_message"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    reviews = reviews[
        reviews[
            "review_comment_message"
        ].str.len() > 0
    ]

    total_final = len(reviews)

    print(
        "\n=== ESTATÍSTICAS DE LIMPEZA ===\n"
    )

    print(
        f"Reviews originais      : "
        f"{total_inicial:,}"
    )

    print(
        f"Reviews sem comentário : "
        f"{sem_texto:,}"
    )

    print(
        f"Reviews finais         : "
        f"{total_final:,}"
    )

    reducao = (
        (
            total_inicial
            - total_final
        )
        / total_inicial
    ) * 100

    print(
        f"Redução total          : "
        f"{reducao:.2f}%"
    )

    return reviews


def enriquecer_reviews(
    reviews,
    orders,
    order_items,
    products,
    categories,
):

    log.info(
        "Executando joins..."
    )

    produtos = products.merge(
        categories,
        on="product_category_name",
        how="left",
    )

    produtos_pedido = (
        order_items.merge(
            produtos[
                [
                    "product_id",
                    "product_category_name_english",
                ]
            ],
            on="product_id",
            how="left",
        )
        .groupby("order_id")
        .agg(
            categorias=(
                "product_category_name_english",
                lambda x: sorted(
                    set(
                        c
                        for c in x
                        if pd.notna(c)
                    )
                ),
            ),
            quantidade_produtos=(
                "product_id",
                "count",
            ),
        )
        .reset_index()
    )

    df = reviews.merge(
        orders[
            [
                "order_id",
                "order_purchase_timestamp",
            ]
        ],
        on="order_id",
        how="left",
    )

    df = df.merge(
        produtos_pedido,
        on="order_id",
        how="left",
    )

    df["ano_compra"] = pd.to_datetime(
        df[
            "order_purchase_timestamp"
        ],
        errors="coerce",
    ).dt.year

    return df


def validar_integridade_pos_join(
    reviews,
    df,
):

    print(
        "\n=== VALIDAÇÃO PÓS-JOIN ===\n"
    )

    total_reviews = len(reviews)
    total_join = len(df)

    print(
        f"Reviews originais : "
        f"{total_reviews:,}"
    )

    print(
        f"Reviews após join : "
        f"{total_join:,}"
    )

    if total_reviews != total_join:

        raise ValueError(
            "Duplicação detectada "
            "após joins."
        )

    review_ids_duplicados = (
        df["review_id"]
        .duplicated()
        .sum()
    )

    print(
        f"Review_id duplicados : "
        f"{review_ids_duplicados:,}"
    )

    if review_ids_duplicados > 0:

        raise ValueError(
            "Review_id duplicados "
            "após joins."
        )

    print(
        "Integridade validada."
    )


def exibir_estatisticas_dataset(df):

    print(
        "\n=== ESTATÍSTICAS DO DATASET ===\n"
    )

    print(
        f"Documentos totais      : "
        f"{len(df):,}"
    )

    categorias_presentes = (
        df["categorias"]
        .notna()
        .sum()
    )

    categorias_ausentes = (
        df["categorias"]
        .isna()
        .sum()
    )

    print(
        f"Categorias encontradas : "
        f"{categorias_presentes:,}"
    )

    print(
        f"Categorias ausentes    : "
        f"{categorias_ausentes:,}"
    )

    anos = sorted(
        df["ano_compra"]
        .dropna()
        .astype(int)
        .unique()
    )

    print(
        f"Anos encontrados       : "
        f"{anos}"
    )


def criar_documento(row):

    categorias = row.get(
        "categorias",
        [],
    )

    categorias_texto = (
        ", ".join(categorias)
        if categorias
        else "unknown"
    )

    return f"""
Categorias: {categorias_texto}

Ano: {row['ano_compra']}

Quantidade de Produtos: {row['quantidade_produtos']}

Nota: {row['review_score']}

Comentário:
{row['review_comment_message']}
""".strip()


def salvar_dataset(df):

    config.DADOS_PROCESSADOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        config.REVIEWS_PROCESSADAS,
        index=False,
    )

    log.info(
        "Arquivo salvo em %s",
        config.REVIEWS_PROCESSADAS,
    )


def preparar():

    dados = carregar_dados()

    validar_colunas(dados)

    reviews = dados["reviews"]
    orders = dados["orders"]
    order_items = dados["order_items"]
    products = dados["products"]
    categories = dados["categories"]

    validar_joins(
        reviews,
        orders,
        order_items,
        products,
    )

    reviews = limpar_reviews(
        reviews
    )

    df = enriquecer_reviews(
        reviews,
        orders,
        order_items,
        products,
        categories,
    )

    validar_integridade_pos_join(
        reviews,
        df,
    )

    exibir_estatisticas_dataset(
        df
    )

    log.info(
        "Criando documentos RAG..."
    )

    df["document"] = df.apply(
        criar_documento,
        axis=1,
    )

    salvar_dataset(df)

    print(
        "\n=== AMOSTRA DOCUMENTO RAG ===\n"
    )

    print(
        df["document"].iloc[0]
    )

    return df


if __name__ == "__main__":
    preparar()
