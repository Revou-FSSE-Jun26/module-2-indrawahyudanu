
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

## Flask intro

### 1 . Instalation and activation VENV
```bash
 python -m venv venv
venv\Scripts\activate 
```

### 2.  Install flask-sqlalchemy psycopg2-binary
```bash
pip install flask-sqlalchemy psycopg2-binary
pip freeze > requirements.txt 
```

### 3. Configure the Database Connection

```bash
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# TODO 1: Set SQLALCHEMY_DATABASE_URI to connect to your local PostgreSQL 'store_db'
# Format: postgresql://username:password@host/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/postgres'

# TODO 2: Set SQLALCHEMY_TRACK_MODIFICATIONS to False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO 3: Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

@app.route('/')
def index():
    return jsonify({"message": "Flask is connected to PostgreSQL!", "status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
```

## API Endpoints & Usage
| Method | Endpoint         | Status Code                     |
| -----  | ------------     | ------------                    |
| GET    | /products        | 200 OK                          |
| GET    | /products/<id>   | 200 OK / 404 Not Found          |
| POST   | /products        | 201 Created / 400 Bad Request   |



## Sampe POST PRODUCT
```bash
{
    "name"        : "Laptop Gmaing ASUS",
    "sku"         : "LTP-001",
    "stock"       : 5,
    "price"       : 15000000,
    "is_in_stock" :true
}
```

## Evidence & Testing
<img width="752" height="508" alt="post product" src="https://github.com/user-attachments/assets/333ee96d-e670-4332-b4fe-baf7d8d2e827" />

