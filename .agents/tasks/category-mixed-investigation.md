# Investigasi: kategori "masih nyampur" di web

## Ringkasan

Penyebab paling mungkin, berurutan:

1. **GET /products tidak punya filter kategori.** `routes/product_routes.py::get_products` hanya mendukung `is_sale` dan `q`. Query seperti `?category_id=2` atau `?category=slug` diabaikan, jadi semua produk dari semua kategori dikembalikan. Gejalanya persis "nyampur".
2. **Data kategori di database berasal dari tiga sumber seed yang berbeda dan tidak konsisten.** Tidak ada satu sumber kebenaran.
3. **Migrasi slug tidak melakukan backfill.** Kategori lama bisa punya `slug = NULL`, sehingga lookup by slug gagal atau frontend jatuh ke perilaku fallback.

Pertanyaan 1 (soft-delete kategori) tidak bermasalah: GET kategori sudah memfilter `is_deleted`.

## Bukti

### Q1. Apakah GET categories memfilter is_deleted? Ya.
- `routes/category_routes.py` `get_all_categories`: `Category.query.filter_by(is_deleted=False)`.
- `get_category` (by id atau slug): filter `is_deleted=False`, dan produk di dalamnya difilter `if not product.is_deleted`.

### Q2. Apakah listing produk memfilter kategori? Tidak.
- `routes/product_routes.py` `get_products`: `Product.query.filter_by(is_deleted=False)`, lalu hanya `is_sale == 'true'` dan `q` (ilike nama). Tidak ada `category_id`, `category`, atau `slug`.
- `Product.to_dict()` di `models.py` memang mengirim `category_id`, `category_name`, `category_slug`. Jadi frontend bisa memfilter sendiri. Kalau frontend memanggil `/products/?category=...` dan mengira server memfilter, hasilnya semua produk.
- Alternatif yang sudah benar di backend: `GET /categories/<id|slug>` mengembalikan produk milik kategori itu. Item produknya tidak memuat `image`, `is_sale`, atau `description`.
- Produk yang kategorinya soft-deleted tetap muncul di `/products`. Tidak ada join atau filter `Category.is_deleted`. Ini juga bisa terlihat sebagai kategori "nyangkut".
- `put_category` dan `create_product` tidak memvalidasi `category_id` (tidak dicek ada atau tidak, atau sudah dihapus). `create_product` juga memvalidasi harga setelah objek dibuat (kosmetik).

### Q3. Seed data
- `seed.py` (`seed_products`): kategori id 1-3 = "Laptop & Aksesoris", "Smartphone & Tablet", "Audio & Aksesoris". Produk ditetapkan dengan `category_id` hard-coded. Seed hanya membuat kategori kalau `Category.query.get(id)` kosong. Kalau id 1-3 sudah berisi kategori lain, produk seed masuk ke kategori yang salah. Contoh: iPhone masuk ke "Pakaian Wanita" kalau `seed.sql` yang jalan duluan.
- `database/seed.sql`: kategori "Pakaian Pria", "Pakaian Wanita", "Elektronik", "Aksesoris", "Sepatu". Kolom `slug` tidak diisi, jadi NULL. Insert users memakai kolom `username`, padahal model memakai `customer_name`, jadi skrip ini sudah usang. `database/sqema.sql` juga usang (tanpa slug, is_deleted, image).
- `seed.json`: 10 kategori lain lagi (Fashion, Electronics, Home & Living, ...). Tidak terlihat ada loader di `seed.py`; tidak diverifikasi apakah ada skrip lain yang memakainya.
- Akibatnya, database bisa berisi gabungan dari tiga set kategori: "Elektronik" vs "Electronics" vs "Smartphone & Tablet", "Aksesoris" vs "Audio & Aksesoris". Ini kandidat kuat penyebab tampilan kategori yang bercampur.
- `name` unique (`models.py`), jadi duplikat persis tidak mungkin. Duplikat semantik (beda ejaan) tetap bisa terjadi.
- `seed.py` memasukkan Category dengan id eksplisit. Di PostgreSQL ini tidak memajukan sequence, jadi POST /categories berikutnya bisa gagal dengan duplicate key pada id. Tidak diverifikasi di runtime.
- `seed.py` juga punya `print("\ Proses ...")` (escape tidak valid, hanya peringatan).

### Q4. Migrasi vs model
- `9374b8d259f0` menambah `slug String(120) nullable=True` plus unique constraint tanpa nama (`create_unique_constraint(None, ['slug'])`). Tidak ada UPDATE backfill. Baris lama tetap `slug = NULL`. Model baru hanya mengisi slug lewat `Category.__init__` untuk objek baru, jadi kategori lama tidak ikut.
- Downgrade-nya memakai `drop_constraint(None, ...)`, yang akan gagal karena nama constraint kosong.
- `1472232c43ba` menambah `is_deleted Boolean server_default='false' nullable=False`. Konsisten dengan model (model memakai `server_default='False'`, setara di PostgreSQL).
- Rantai revisi: ca75c04feb18 -> 1472232c43ba, lalu c633d673493e -> 9374b8d259f0. Perlu dipastikan hanya ada satu head, dengan `flask db heads`. Tidak dijalankan.
- `git status` menunjukkan `models.py` sudah dimodifikasi dan belum di-commit. Kolom `image` pada Category tidak terlihat di migrasi yang ada (hanya dua migrasi yang dibaca) dan perlu dicek di migrasi lain. Kalau tidak ada, query `Category` akan error di database yang belum diupgrade.

### Q5. Penyebab lain yang mungkin
- Frontend memakai cache lama, atau memakai endpoint `/categories` dan `/products` dengan filter di sisi klien berdasarkan `category_name`. Dengan nama yang tidak konsisten (lihat Q3), pengelompokan akan terlihat acak.
- Database yang dicek frontend (lokal vs deploy) bisa berbeda dari yang di-seed. Ini tidak bisa diverifikasi tanpa akses runtime.
- `routes/routes.py` hanya berisi home route, bukan penyebab.

## Yang tidak bisa diverifikasi
- Isi database sebenarnya (tidak membuka `.env` atau menghubungkan ke DB), URL yang dipanggil frontend, hasil `flask db heads`, dan ada tidaknya migrasi untuk kolom `categories.image`.

## Kesimpulan dan rekomendasi (belum diimplementasikan)
1. Tambahkan filter kategori di `get_products`: `category_id` (int) dan `category` (slug) dengan join ke `Category` dan `Category.is_deleted == False`. Ini perbaikan utama.
2. Putuskan satu set kategori resmi, lalu bersihkan database: soft-delete atau gabungkan kategori sisa seed lama, dan pindahkan `category_id` produk yang salah.
3. Satukan seed: buat `seed.py` mencari kategori by name (bukan id hard-coded), isi slug, dan hapus atau perbarui `seed.sql`, `sqema.sql`, dan `seed.json`.
4. Tambahkan migrasi data untuk backfill slug dari `name` pada baris yang `slug IS NULL`, lalu pertimbangkan `nullable=False`. Beri nama pada unique constraint.
5. Validasi `category_id` (ada dan tidak terhapus) di POST dan PUT product.
6. Setelah seed dengan id eksplisit di PostgreSQL, reset sequence (`setval`).
7. Minta user menyebutkan URL yang dipanggil frontend untuk memastikan penyebab #1 versus data (#2).
