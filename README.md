# REVO SHOP BACKEND PROJECT

## Overview
Revoshop Merupakan platform RESTful API yang dirancang untuk mendukung ekosistem *e-commerce* . API ini menangani seluruh logika bisnis utama, mulai dari autentikasi pengguna, manajemen katalog produk, hingga pemrosesan transaksi pemesanan (*orders*).
Backend ini dibangun menggunakan **Flask (Python)** dengan arsitektur modular (*Blueprints*), memanfaatkan **JSON** sebagai format pertukaran data (*data interchange format*), serta menggunakan **PostgreSQL** sebagai sistem manajemen basis data relasional.

## Live Deployment
https://revoshop-indra-wahyu.onrender.com/

## Feature
* **CRUD Lengkap**: Mendukung pembuatan, pembacaan, pembaruan, dan penghapusan data untuk User, Produk, Kategori, dan Order.
* **Relasi Many-to-Many**: Menghubungkan Produk dan Order melalui tabel perantara `order_items`.
* **Validasi Data**: Memastikan input data sesuai format sebelum diproses ke database.
* **Penanganan Error**: Menggunakan blok `try/except` untuk menangkap error dan memberikan respons yang tepat agar input dari client sesuai yang diharapkan.

## Tech Stack
* **Python** 3.14.6
* **Flask** 3.1.3 (Web Framework)
* **Werkzeug** 3.1.8 (Hashing Password)
* **PostgreSQL** & **pgAdmin** (Database & Database Management)
* **Flask-SQLAlchemy** 2.0.52 (ORM)
* **Flask-Migrate** 4.1.0 (Database Migration)
* **pytest** (Testing Framework)
* **Locust** (Load Testing)
* **python-dotenv** (Environment Variable Management)
* **Postman** (API Testing & Documentation)

## Project Structure

```text
├── images/                 # Dokumentasi visual (Tangkapan layar API, diagram, & ERD)
├── migrations/             # Folder migrasi database (Managed by Flask-Migrate / Alembic)
├── app.py                  # Entry point (Application Factory & Blueprint Registration)
├── config.py               # Konfigurasi aplikasi & database dari file .env
├── models.py               # Model ORM (User, Category, Product, Order, OrderItem) & to_dict()
├── utils.py                # Inisialisasi shared instance (db & migrate)
│
├── routes/                 # Folder Endpoints / Blueprints
│   ├── auth_routes.py      # POST /login (JWT access & refresh token)
│   ├── user_routes.py      # POST /users (register), GET /users/<id>
│   ├── product_routes.py   # CRUD Product (Soft Delete & Validasi Harga)
│   ├── category_routes.py  # CRUD Category (Include relasi produk)
│   ├── order_routes.py     # CRUD Order & OrderItem (Protected @jwt_required)
│   └── routes.py           # Home / Demo route
│
├── database/               # Skrip SQL & Database Tools
│   ├── schema.sql          # DDL Skema tabel database
│   ├── seed.sql            # DML Dummy data untuk pengujian
│   └── queries.sql         # Contoh SQL query analitis
│
├── tests/                  # Pengujian Aplikasi
│   └── pytest.ini          # Konfigurasi runner Pytest
│
├── .env                    # Environment variables (DB URL, JWT Secret)
├── .gitignore              # Mengabaikan venv, .env, __pycache__, dll.
├── requirements.txt        # Dependency lengkap (Production & Testing)
├── requirements_dev.txt    # Dependency khusus lingkungan Development
└── audit.sh                # Shell script opsional 
```

## How to run the project locally 

### 1. Clone Referensi Repository 
```bash
git clone https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu.git
cd revoshop-db
```

### 2. Instalasi dan aktivasi VENV
```bash
python -m venv venv
venv\Scripts\activate 
```

### 3. Instalasi Depedency
```bash
pip install -r requirements.txt
```

### 4. Mengatur Environment Variable
Buat file `.env` di direktori utama (root) proyek, lalu isi seperti berikut:
```env
   DATABASE_URL=postgresql://postgres:password_kamu@localhost:5432/nama_db_kamu
   JWT_SECRET_KEY=rahasia_bebas
```

### 5. Migrasi Data
```bash 
flask db upgrade
 ```

### 6. Flask Run
```bash 
flask run
```

## API Endpoints & Usage
##  API Endpoints

Aplikasi ini menggunakan format **JSON** untuk *request* dan *response*. Sebagian besar *endpoint* memerlukan autentikasi **JWT (Bearer Token)** yang dikirim melalui *Header*: `Authorization: Bearer 

### Authentication (`/login`)

| Method | Endpoint | Auth | Deskripsi |
| :--- | :--- | :---: | :--- |
| `POST` | `/users` | ❌ | Pendaftaran akun pengguna baru |
| `POST` | `/login` | ❌ | Otentikasi pengguna & mendapatkan Token JWT |

---

### Products (`/products`)

| Method | Endpoint | Auth | Deskripsi |
| :--- | :--- | :---: | :--- |
| `GET` | `/products` | ❌ | Mengambil seluruh daftar produk |
| `GET` | `/products/<id>` | ❌ | Mengambil detail 1 produk berdasarkan ID |
| `POST` | `/products` | ❌ | Menambahkan produk baru ke database |
| `PUT` | `/products/<id>` | ❌ | Memperbarui data produk berdasarkan ID |
| `DELETE` | `/api/products/<id>` | ❌ | Menghapus produk |

---

### Category (`/category`)

| Method | Endpoint | Auth | Deskripsi |
| :--- | :--- | :---: | :--- |
| `GET` | `/categories` | ❌ | Mengambil seluruh daftar produk |
| `GET` | `/categories/<id>` | ❌ | Mengambil detail 1 produk berdasarkan ID |
| `POST` | `/categories` | ❌ | Menambahkan produk baru ke database |
| `PUT` | `/categories/<id>` | ❌ | Memperbarui data produk berdasarkan ID |
| `DELETE` | `/categories/<id>` | ❌ | Menghapus produk |

---

###  Orders (`/orders`)

| Method | Endpoint | Auth | Deskripsi |
| :--- | :--- | :---: | :--- |
| `GET` | `/orders` | 🔒 | Melihat riwayat transaksi/order milik pengguna |
| `POST` | `/orders` | 🔒 | Membuat order baru (termasuk entri ke `order_items`) |
| `GET` | `/orders/<id>` | 🔒 | Melihat detail rincian order berdasarkan ID |
| `DELETE` | `/orders/<id>` | 🔒 | Menghapus produk |


##  Screenshots & Documentation
[API base URL](https://revoshop-indra-wahyu.onrender.com/)

###  API Documentation
Dokumentasi lengkap API beserta contoh request dan response untuk setiap endpoint (GET, POST, PUT, DELETE) :
[Postman API Documentation](https://documenter.getpostman.com/view/57428406/2sBYAvwAuD)

---
###  DATABASE Documentation

Database View (Dbreaver)
[Screenshots dbreaver](https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu/blob/main/image/GET%20one%20product%20by%20ID.png)

Tabel Categories
[Screenshots Tabel Categories](https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu/blob/main/image/Tabel%20Categories.PNG)

Tabel Order Item
[Screenshots order_item](https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu/blob/main/image/tabel%20orders%20item.PNG)

Tabel Orders
[Screenshots Tabel Orders](https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu/blob/main/image/Tabel%20orders.PNG)

Tabel Products
[Screenshots Tabel Products](https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu/blob/main/image/tabel%20products.PNG)

Tabel Users
[Screenshots Tabel Users](https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu/blob/main/image/tabel%20users.PNG)

---

### Load Testing (Locust)

Load Testing
[Screenshots Load Testing](https://github.com/Revou-FSSE-Jun26/module-2-indrawahyudanu/blob/main/image/Locust%20test.PNG)


