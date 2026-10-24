from sqlalchemy import create_engine

host = 'localhost'
port = 5432
user = 'postgres'
password = 'postgres'
database = 'fake_store_db'

def load_to_postgres(df, table_name):
    """
    Load a pandas DataFrame to a PostgreSQL table.

    Args:
        df (pandas.DataFrame): The DataFrame to be loaded.
        table_name (str): The name of the table to load the data into.
    """
    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
        df.to_sql(table_name,
                engine,
                if_exists='append',
                index=False)

        print(f"Data loaded to {table_name} table in PostgreSQL database {database}.")
    except Exception as e:
        print(f"Error occurred while loading data to {table_name} table: {e}")