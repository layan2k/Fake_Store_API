import pandas as pd

def transform_product(product_df: pd.DataFrame) -> pd.DataFrame:
    df = product_df.copy()

    df = df.rename(columns={'id': 'product_id',
                            'title': 'product_title',
                            'price': 'product_price',
                            'description': 'product_description',
                            'category': 'product_category'
                            })
    df = df[['product_id', 'product_title', 'product_price', 'product_description',  'product_category']]
    df['product_price'] = df['product_price'].astype(float)

    return df

def transform_users(users_df: pd.DataFrame) -> pd.DataFrame:
    df = users_df.copy()

    df['first_name'] = df['name'].apply(lambda x: x['firstname'])
    df['last_name'] = df['name'].apply(lambda x: x['lastname'])
    df['street'] = df['address'].apply(lambda x: x['street'])
    df['city'] = df['address'].apply(lambda x: x['city'])
    df['zipcode'] = df['address'].apply(lambda x: x['zipcode'])

    df = df.rename(columns={'id': 'user_id',
                            'email': 'user_email',
                            'username': 'username'
                            })

    df = df[['user_id', 'first_name', 'last_name', 'user_email', 'username', 'street', 'city', 'zipcode']]
    return df