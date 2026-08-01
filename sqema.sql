--1. Table users
CREATE TABLE users (
    user_id       SERIAL PRIMARY KEY,
    username      VARCHAR(50)    NOT NULL UNIQUE,
    email         VARCHAR(100)   NOT NULL UNIQUE,
    created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

--2. Table categories
CREATE TABLE categories (
    category_id  SERIAL PRIMARY KEY,
    name           VARCHAR(100)    NOT NULL UNIQUE
);

--3. Table products
CREATE TABLE products (
    product_id    SERIAL PRIMARY KEY,
    product_name  VARCHAR(100)   NOT NULL,
    price         DECIMAL(10, 2) NOT NULL,
    stock         INTEGER        NOT NULL,
    category_id   INTEGER        REFERENCES categories(category_id),
    created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

--4. Table orders
CREATE TABLE orders (
    order_id        SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(user_id),
    total_amount    NUMERIC (10, 2) NOT NULL
);

--5. table order_items
CREATE TABLE order_items (
    order_item_id  SERIAL PRIMARY KEY,
    order_id       INTEGER REFERENCES orders(order_id),
    product_id     INTEGER REFERENCES products(product_id),
    quantity       INTEGER NOT null,
    subtotal       numeric not null
);