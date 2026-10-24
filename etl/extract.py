import pandas as pd
import requests

BASE_URL = "https://fakestoreapi.com"

def extract_product() -> pd.DataFrame:
    url = f'{BASE_URL}/products'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    product_df = pd.DataFrame(data)
    return product_df


def extract_users() -> pd.DataFrame:
    url = f'{BASE_URL}/users'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    users_df = pd.DataFrame(data)
    return users_df

