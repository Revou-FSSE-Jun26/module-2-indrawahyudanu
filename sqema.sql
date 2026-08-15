-- 1. Table users
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50)    NOT NULL UNIQUE,
    email         VARCHAR(255)   NOT NULL UNIQUE,
    created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table categories
CREATE TABLE categories (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100)   NOT NULL UNIQUE
);

-- 3. Table products
CREATE TABLE products (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100)   NOT NULL,
    sku           VARCHAR(50)    NOT NULL UNIQUE,
    price         NUMERIC(10, 2) NOT NULL,
    stock         INTEGER        NOT NULL DEFAULT 0,
    is_in_stock   BOOLEAN        NOT NULL TRUE,
    category_id   INTEGER        REFERENCES categories(id),
    created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

-- 4. Table orders 
CREATE TABLE orders (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER        REFERENCES users(id),
    total_amount    NUMERIC(10, 2) NOT NULL,
    order_date      TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

-- 5. Table order_items 
CREATE TABLE order_items (
    id             SERIAL PRIMARY KEY,
    order_id       INTEGER        REFERENCES orders(id),
    product_id     INTEGER        REFERENCES products(id),
    quantity       INTEGER        NOT NULL,
    subtotal       NUMERIC(10, 2) NOT NULL
);