# REVO SHOP DATABASE PROJECT

You've just joined RevoShop as a backend developer. Before writing a single line of application code, your first task is to design and validate the database that will power the entire store: users, products, categories, orders, and the line items that link orders to products.

## File Structure
- `schema.sql`: Contains DDL scripts to create tables (`users`, `categories`, `products`, `orders`, and `order_items`).
- `seed.sql`: Contains DML scripts to insert sample data (dummy data).
- `queries.sql`: Contains SQL queries using `SELECT`, `WHERE`, `JOIN`, `ORDER BY`, and `LIMIT` for data analysis.
- `app.py`: Serves as the main application entry point, containing Databse initialization, Route Model connection and Development server.
- `config.py` : Contains the database connection settings and application configurations. Key responsibilities include : Database URL Configuration and ORM Settings.
- `models.py` : defines the database schema, table structures, relationships, and JSON serialization methods using SQLAlchemy ORM.
- `routes.py` : Handles API endpoints, HTTP requests (GET, POST), business logic, and JSON responses.


## How to Use
1. Run `schema.sql` on PostgreSQL to set up the database tables.
2. Run `seed.sql` to populate the tables with sample data.
3. Run `queries.sql` to view and analyze the data.

<img width="1298" height="787" alt="diagram" src="https://github.com/user-attachments/assets/f00218be-3b32-4116-96b2-3be3b3874d80" />

## Flask intro

### 1 . Instalation VENV
BASH python -m venv venv
venv\Scripts\activate BASH
