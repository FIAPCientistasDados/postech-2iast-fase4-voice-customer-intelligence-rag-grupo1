## Ler os CSVs

import pandas as pd

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

orders = pd.read_csv(
    "data/raw/olist_orders_dataset.csv"
)

products = pd.read_csv(
    "data/raw/olist_products_dataset.csv"
)
