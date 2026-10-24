from etl.extract import extract_product, extract_users
from etl.transform import transform_product, transform_users
from etl.load import load_to_postgres

def run_pipeline():
    print("Starting ETL pipeline...")

    print("Extracting data from API...")
    product_df = extract_product()
    users_df = extract_users()

    print("Transforming data...")
    product_df = transform_product(product_df)
    users_df = transform_users(users_df)

    print("Loading data into PostgreSQL...")
    load_to_postgres(product_df, 'products')
    load_to_postgres(users_df, 'users')

    print("ETL pipeline completed.")


if __name__ == "__main__":
    run_pipeline()


