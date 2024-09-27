import os
import pandas as pd

import minsearch


DATA_PATH = os.getenv("DATA_PATH", "../data/data.csv")


def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)
    # Convert 'price' and 'calories' to string
    df['price'] = df['price'].astype(str)
    df['calories'] = df['calories'].astype(str)
    
    documents = df.to_dict(orient="records")

    index = minsearch.Index(
        text_fields=[
            "name",
            "cuisine",
            "type",
            "ingredients",
            "serving",
            "price",
            "calories",
        ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index