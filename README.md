# Fake Store API ETL

A small Python ETL pipeline that extracts products and users from
[Fake Store API](https://fakestoreapi.com/), transforms the nested API
responses into relational data, and appends the results to PostgreSQL.

## Data flow

1. `etl/extract.py` requests:
   - `https://fakestoreapi.com/products`
   - `https://fakestoreapi.com/users`
2. `etl/transform.py` flattens the product and user payloads.
3. `etl/load.py` writes the transformed data to the `products` and `users`
   tables in PostgreSQL.

The pipeline uses `if_exists='append'`, so each run appends rows rather than
replacing existing table data.

## Requirements

- Python 3.9+
- PostgreSQL
- A PostgreSQL driver supported by SQLAlchemy (`psycopg2-binary` is used by
  the default `postgresql://` connection URL)

Install the Python dependencies:

```bash
python -m pip install pandas requests sqlalchemy psycopg2-binary
```

## PostgreSQL setup

Create the database before running the pipeline:

```sql
CREATE DATABASE fake_store_db;
```

The current loader connects with these values:

| Setting | Default |
| --- | --- |
| Host | `localhost` |
| Port | `5432` |
| User | `postgres` |
| Password | `postgres` |
| Database | `fake_store_db` |

These values are defined in `etl/load.py`. Update them before running the
pipeline if your local PostgreSQL configuration is different. Do not commit
real production credentials to source control.

## Run the pipeline

From the project root:

```bash
python main.py
```

Expected output includes:

```text
Starting ETL pipeline...
Extracting data from API...
Transforming data...
Loading data into PostgreSQL...
ETL pipeline completed.
```

## Tables

Pandas creates the tables on the first successful load. The resulting columns
are:

### `products`

| Column | Description |
| --- | --- |
| `product_id` | Product identifier from the API |
| `product_title` | Product name |
| `product_price` | Product price |
| `product_description` | Product description |
| `product_category` | Product category |

### `users`

| Column | Description |
| --- | --- |
| `user_id` | User identifier from the API |
| `first_name` | User's first name |
| `last_name` | User's last name |
| `user_email` | User's email address |
| `username` | User's username |
| `street` | Street address |
| `city` | City |
| `zipcode` | Postal code |

## Database verification queries

Connect to the database first:

```bash
psql -h localhost -p 5432 -U postgres -d fake_store_db
```

Check that the expected tables exist:

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('products', 'users')
ORDER BY table_name;
```

Inspect the table definitions:

```sql
\d+ products
\d+ users
```

Count loaded rows:

```sql
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
UNION ALL
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM users;
```

Preview the loaded data:

```sql
SELECT *
FROM products
ORDER BY product_id
LIMIT 10;

SELECT *
FROM users
ORDER BY user_id
LIMIT 10;
```

Check for duplicate source identifiers:

```sql
SELECT product_id, COUNT(*) AS duplicate_count
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, product_id;

SELECT user_id, COUNT(*) AS duplicate_count
FROM users
GROUP BY user_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, user_id;
```

Check for missing required values:

```sql
SELECT COUNT(*) AS invalid_products
FROM products
WHERE product_id IS NULL
   OR product_title IS NULL
   OR product_price IS NULL
   OR product_category IS NULL;

SELECT COUNT(*) AS invalid_users
FROM users
WHERE user_id IS NULL
   OR first_name IS NULL
   OR last_name IS NULL
   OR user_email IS NULL
   OR username IS NULL;
```

Check product price and category distributions:

```sql
SELECT
    MIN(product_price) AS minimum_price,
    MAX(product_price) AS maximum_price,
    ROUND(AVG(product_price), 2) AS average_price
FROM products;

SELECT product_category, COUNT(*) AS product_count
FROM products
GROUP BY product_category
ORDER BY product_count DESC, product_category;
```

Because the pipeline appends on every run, use these queries to identify
repeated loads:

```sql
SELECT product_id, COUNT(*) AS load_count
FROM products
GROUP BY product_id
ORDER BY load_count DESC, product_id
LIMIT 20;
```

## Project structure

```text
.
├── etl/
│   ├── extract.py
│   ├── load.py
│   └── transform.py
├── main.py
└── README.md
```

## Notes

- The upstream API must be reachable when the pipeline runs.
- The extract functions call `raise_for_status()`, so HTTP errors stop the
  extraction step.
- The loader currently catches load exceptions and prints them. Check the
  command output and the verification queries to confirm that both tables were
  populated successfully.