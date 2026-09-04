# REVO SHOP BACKEND PROJECT

## Overview
Revoshop Merupakan platform RESTful API yang dirancang untuk mendukung ekosistem *e-commerce* . API ini menangani seluruh logika bisnis utama, mulai dari autentikasi pengguna, manajemen katalog produk, hingga pemrosesan transaksi pemesanan (*orders*).
Backend ini dibangun menggunakan **Flask (Python)** dengan arsitektur modular (*Blueprints*), memanfaatkan **JSON** sebagai format pertukaran data (*data interchange format*), serta menggunakan **PostgreSQL** sebagai sistem manajemen basis data relasional.

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

##  Screenshots & Documentation

###  API Documentation
Dokumentasi lengkap API beserta contoh request dan response untuk setiap endpoint (GET, POST, PUT, DELETE) :
[Postman API Documentation](https://documenter.getpostman.com/view/57428406/2sBYAvwAuD)

---

### 🗄️ Database View (Dbreaver)
Tampilan tabel-tabel lokal pada Database Dbreaver setelah dilakukan migrasi:
[Lihat Folder Screenshots pgAdmin][.image\Diagram Table All.PNG]

---

### 📊 Load Testing (Locust - Opsional)


## API Endpoints & Usage
| Method | Endpoint         | Status Code                     |
| -----  | ------------     | ------------                    |
| GET    | /products        | 200 OK                          |
| GET    | /products/<id>   | 200 OK / 404 Not Found          |
| POST   | /products        | 201 Created / 400 Bad Request   |



## Sampe POST product table
```bash
 {
        "name": "Monitor Lenovo",
        "sku" : "MO_Lenovo_1",
        "price": 15000000.0,
        "stock" : "10",
        "category_id" : "3"
        
    }


## Evidence 

### Testing POST product
image/post product.png
<img src="image/post product.png" width="500" alt="evidence">

### Testing GET all products
<img src="image/Get Product.png" width="500" alt="evidence GET all products">

### Testing GET products by ID
<img src="image/GET%20one%20product%20by%20ID.png" width="500" alt="Evidence & Testing GET products by ID">

### Testing Handling Error 404
<img src="image/Handling%20error%20404.PNG" width="500" alt="Evidence Testing Handling Error">

## Sampe POST user table
```bash
{
    "username":"Bambang_pamungkas",
    "email":"bambangp@email.com",
    "role" : "customer",
    "password" : "rahasiadong"
    
}
```
### Testing POST user
<img src="image/post%20user.png" width="500" alt="evidence">

### Testing GET user by ID
<img src="image/GET%20user%20by%20ID.PNG" width="500" alt="evidence">

### Testing Handling Error 404
<img src="image/Handling%20error%20user.PNG" width="500" alt="evidence">

### Adding role to Database
<img src="image/role in dbrever.PNG" width="500" alt="evidence">


[def]: ./image