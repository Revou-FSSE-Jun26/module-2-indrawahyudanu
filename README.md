#REVOSHOP DATABASE PROJECT#
 You've just joined RevoShop as a backend developer. Before writing a single line of application code, your first task is to design and validate the database that will power the entire store: users, products, categories, orders, and the line items that link orders to products.

## Structure File ##
- `schema.sql`: Contains DDL for making tabel `users`, `categories`, `products`, `orders`, and `order_items`.
- `seed.sql`: contain DML for fill (dummy data).
- `queries.sql` : contains  (SELECT, WHERE, JOIN, ORDER BY, LIMIT) for analysis the data.

## HOW TO USE##
1. RUN `schema.sql` on PostgreSQL.
2. RUN `seed.sql` For fill the table.
3. RUN `queries.sql` For show the data.