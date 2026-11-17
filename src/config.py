"""
Configurações globais do projeto.
"""

from pathlib import Path
import os

# ==================================================
# DIRETÓRIOS
# ==================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

DADOS_BRUTOS = DATA_DIR / "raw"
DADOS_PROCESSADOS = DATA_DIR / "processed"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

LOGS_DIR = ROOT_DIR / "logs"

# ==================================================
# DATASET OLIST
# ==================================================

KAGGLE_DATASET = "olistbr/brazilian-ecommerce"

ARQUIVOS_OLIST = [
    "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "product_category_name_translation.csv",
]

# ==================================================
# ARQUIVOS PRINCIPAIS
# ==================================================

ARQUIVO_CUSTOMERS = (
    DADOS_BRUTOS / "olist_customers_dataset.csv"
)

ARQUIVO_ORDER_ITEMS = (
    DADOS_BRUTOS / "olist_order_items_dataset.csv"
)

ARQUIVO_REVIEWS = (
    DADOS_BRUTOS / "olist_order_reviews_dataset.csv"
)

ARQUIVO_ORDERS = (
    DADOS_BRUTOS / "olist_orders_dataset.csv"
)

ARQUIVO_PRODUCTS = (
    DADOS_BRUTOS / "olist_products_dataset.csv"
)

ARQUIVO_CATEGORY_TRANSLATION = (
    DADOS_BRUTOS /
    "product_category_name_translation.csv"
)

# ==================================================
# SAÍDAS PROCESSADAS
# ==================================================

REVIEWS_PROCESSADAS = (
    DADOS_PROCESSADOS / "reviews_processadas.csv"
)

DOCUMENTOS_RAG = (
    DADOS_PROCESSADOS / "documentos_rag.parquet"
)

# ==================================================
# EMBEDDINGS
# ==================================================

EMBEDDING_MODEL = "BAAI/bge-m3"

# Alternativas:
# EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
# EMBEDDING_MODEL = (
#     "sentence-transformers/"
#     "paraphrase-multilingual-MiniLM-L12-v2"
# )

# ==================================================
# CHROMADB
# ==================================================

CHROMA_COLLECTION = "olist_reviews"

TOP_K_DOCUMENTOS = 5

SIMILARIDADE_MINIMA = 0.75

# ==================================================
# OPENAI
# ==================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

OPENAI_MODEL = "gpt-4o-mini"

# ==================================================
# OLLAMA
# ==================================================

OLLAMA_MODEL = "llama3.1"

# ==================================================
# STREAMLIT
# ==================================================

APP_TITLE = (
    "Voice of Customer Intelligence"
)

APP_SUBTITLE = (
    "Tech Challenge Fase 4"
)

# ==================================================
# CRIAÇÃO DE PASTAS
# ==================================================

for pasta in [
    DATA_DIR,
    DADOS_BRUTOS,
    DADOS_PROCESSADOS,
    VECTOR_DB_DIR,
    LOGS_DIR,
]:
    pasta.mkdir(
        parents=True,
        exist_ok=True,
    )
