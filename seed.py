from utils import db
from models import Product, Category  # Sesuaikan lokasi impor modelmu
from app import create_app

app = create_app()

# Daftar 5 produk untuk seeding
PRODUCTS_DATA = [
    {
        "name": "Samsung Galaxy Z Fold 8",
        "sku": "samsung_galaxy_z_fold_8",
        "stock": 12,
        "price": 40500000,
        "category_id": 2
    },
    {
        "name": "iPhone 16 Pro Max",
        "sku": "iphone_16_pro_max",
        "stock": 20,
        "price": 24999000,
        "category_id": 2
    },
    {
        "name": "MacBook Pro M3 Max",
        "sku": "macbook_pro_m3_max",
        "stock": 8,
        "price": 39999000,
        "category_id": 1
    },
    {
        "name": "Sony WH-1000XM5 Headphone",
        "sku": "sony_wh1000xm5",
        "stock": 15,
        "price": 5999000,
        "category_id": 3
    },
    {
        "name": "Logitech MX Master 3S Mouse",
        "sku": "logitech_mx_master_3s",
        "stock": 30,
        "price": 1699000,
        "category_id": 1
    }
]

def seed_products():
    with app.app_context():
        # Opsional: Pastikan kategori dasar ada terlebih dahulu agar Foreign Key tidak error
        categories = [
            {"id": 1, "name": "Laptop & Aksesoris"},
            {"id": 2, "name": "Smartphone & Tablet"},
            {"id": 3, "name": "Audio & Aksesoris"}
        ]
        
        for cat in categories:
            existing_cat = Category.query.get(cat["id"])
            if not existing_cat:
                new_cat = Category(id=cat["id"], name=cat["name"])
                db.session.add(new_cat)
        
        db.session.commit()

        # Proses seeding produk
        for data in PRODUCTS_DATA:
            existing_product = Product.query.filter_by(sku=data["sku"]).first()
            if not existing_product:
                product = Product(
                    name=data["name"],
                    sku=data["sku"],
                    stock=data["stock"],
                    price=data["price"],
                    category_id=data["category_id"]
                )
                db.session.add(product)
                print(f" Berhasil ditambahkan: {data['name']}")
            else:
                print(f"  Produk dengan SKU '{data['sku']}' sudah ada.")

        db.session.commit()
        print("\ Proses seeding produk selesai!")

if __name__ == '__main__':
    seed_products()