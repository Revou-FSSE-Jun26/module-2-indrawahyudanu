# Implementation Plan: category filter fix (GET /products)

Scope: `routes/product_routes.py`, one new migration, `tests/test_product.py`. Never touch seed files (seed.py, seed.sql, seed.json, sqema.sql). Never read `.env`. Never run the migration against the user's DB.

## Findings from exploration
- `get_products` (routes/product_routes.py) uses `Product.query.filter_by(is_deleted=False)` plus `is_sale`/`q` only. Response is `jsonify([p.to_dict() ...]), 200`; errors are `{"error": str(e)}`.
- `create_product` error style: `{"message", "error", "status": "error"}` with 400. It saves the uploaded image BEFORE building the Product, and its broad `except` returns 400. `update_product` is the function literally named `get_product_by_id` (PUT `/<int:product_id>`): errors are `{"error": ...}` (404 not found, 500 generic). Keep that function name.
- `models.py`: `Category` has `name` (unique), `slug` (unique, nullable), `is_deleted`, `image`. `Product.category_id` FK is nullable. `slugify` lives in `utils.py` (NFKD to ascii, strip chars not `\w\s-`, collapse `[-\s]+` to `-`, strip `-_`), NOT in models.py (models only imports it).
- Alembic chain is linear: ca75c04feb18 -> 1472232c43ba -> 15d8b32ba47d -> c633d673493e -> 9374b8d259f0. The single head is `9374b8d259f0` (confirmed by reading every `down_revision`). Nothing else revises it. Note: no migration adds `categories.image` (out of scope; mention in final summary only).
- Tests: `tests/conftest.py` has module-scoped `app` (SQLite in-memory, one Category "Electronics" id=1, one Product "iphone") and `client` fixtures. Existing `test_create_real_product` posts `category_id: 2`, which does not exist in the fixture, so it WILL fail once validation is added and must be fixed (item 4).

## Design decisions
- Category matching: `category` param matches `lower(Category.slug) == v.lower()` OR `lower(Category.name) == v.lower()`, with `v` stripped. One OR clause, so `?category=tv` works for slug "tv" or name "TV". Chosen over slugifying the input because it is simpler and covers both cases.
- Joins: a single `outerjoin(Category, Product.category_id == Category.id)` is always applied. The general list filters `or_(Product.category_id.is_(None), Category.is_deleted.is_(False))`, so null-category products still show and soft-deleted-category products are hidden. When a category filter is present, the added conditions on Category columns naturally exclude null-category rows, and the `is_deleted == False` requirement is satisfied by the same general filter plus an explicit `Category.is_deleted == False` for clarity. Response shape is unchanged.
- Invalid `category_id` (non-int) on GET: 400 `{"error": "category_id must be an integer"}` (existing GET style). If both `category_id` and `category` are given, both apply (AND).
- Write validation: shared helper `_check_category(category_id)` returning `None` if OK, else a `(kind, message)` tuple that each endpoint converts to its own error style. Non-integer value is 400; nonexistent or soft-deleted category is 404 (message "category not found"). On create, validate only when `category_id` is not None (the column is nullable, and omitting it stays allowed). On update, validate only when the key `category_id` is present in the payload and not None. Otherwise behavior is unchanged.
- Migration is self-contained: it inlines a copy of the `utils.slugify` logic rather than importing app code (migrations must stay frozen if utils changes). It uses lightweight `sa.table`/`sa.column` constructs, so it works on PostgreSQL and SQLite.

## Items

- [ ] 1. Add category filtering and soft-deleted-category hiding to `get_products`.
      In `routes/product_routes.py`: change the import to `from models import Product, Category`; add `from sqlalchemy import or_, func`. Rewrite the query inside the existing try as:
      `query = Product.query.outerjoin(Category, Product.category_id == Category.id).filter(Product.is_deleted == False, or_(Product.category_id.is_(None), Category.is_deleted == False))`.
      Keep the `is_sale == 'true'` filter (use `Product.is_sale.is_(True)` / `Product.is_sale == True`, since `filter_by` after a join would bind to the last joined entity, so do NOT use `filter_by` after the join) and the `q` ilike filter unchanged in behavior.
      Parse `category_id = request.args.get('category_id')`: if not None/empty, `int()` it inside a try; on ValueError return `jsonify({"error": "category_id must be an integer"}), 400`; then `query = query.filter(Product.category_id == cid, Category.is_deleted == False)`.
      Parse `category = (request.args.get('category') or '').strip()`: if set, `v = category.lower()`; `query = query.filter(Category.is_deleted == False, or_(func.lower(Category.slug) == v, func.lower(Category.name) == v))`.
      Files: routes/product_routes.py
      Verify: `venv\Scripts\python.exe -m pytest tests -q` (after item 4 adds tests; before that, existing GET test still passes).

- [ ] 2. Validate `category_id` in `create_product` and `update_product` (`get_product_by_id`).
      Add helper `_check_category(raw)` in `routes/product_routes.py` above the routes: `int()` it (ValueError/TypeError -> return `(400, "category_id must be an integer")`; note `bool` is not acceptable, reject `True/False`), then `Category.query.filter_by(id=cid, is_deleted=False).first()`; missing -> `(404, "category not found")`; else `None`.
      create_product: right after `data = ...` and BEFORE the image save (so no orphan file is written), if `data.get('category_id') is not None`, call the helper and on error `return jsonify({"message": "invalid category", "error": msg, "status": "error"}), code`.
      update_product: after `data` is read and BEFORE the image save, if `data.get('category_id') is not None`, call the helper and on error `return jsonify({"error": msg}), code`.
      Everything else in both functions stays unchanged.
      Files: routes/product_routes.py
      Verify: `venv\Scripts\python.exe -m pytest tests -q` passes (including item 4 tests for create/update validation).

- [ ] 3. Add the data migration that backfills `categories.slug`.
      Create `migrations/versions/<new12hex>_backfill_category_slugs.py` (pick a fresh 12-hex revision id, e.g. `a1c4e7d29b53`; confirm it collides with none of the existing ids). Header: `revision = '<id>'`, `down_revision = '9374b8d259f0'`, `branch_labels = None`, `depends_on = None`.
      `upgrade()`: inline `_slugify(text)` = NFKD ascii, lowercase, `re.sub(r'[^a-z0-9]+', '-', text).strip('-')` (spec: non-alphanumerics become `-`, trim `-`). Build `categories = sa.table('categories', sa.column('id', sa.Integer), sa.column('name', sa.String), sa.column('slug', sa.String))`. With `bind = op.get_bind()`: select all `(id, slug)` to build a `taken` set of existing non-empty slugs (lowercase); select rows `WHERE slug IS NULL OR slug = ''` ordered by id; for each, `base = _slugify(name) or f"category-{id}"`; if `base in taken`, `candidate = f"{base}-{id}"`; add to `taken`; `bind.execute(categories.update().where(categories.c.id == id).values(slug=candidate))`. Make the `-<id>` fallback respect the String(120) limit by truncating `base` to `120 - len(str(id)) - 1` chars when appending the suffix (and truncating base to 120 otherwise).
      `downgrade()`: `pass` (no-op). No schema change, no `batch_alter_table`.
      Do NOT run `flask db upgrade` against the user's DB. Files: migrations/versions/<id>_backfill_category_slugs.py
      Verify (safe, throwaway DB only): (a) `venv\Scripts\python.exe -c "import ast,sys;ast.parse(open(r'migrations/versions/<file>.py').read())"` and confirm only one head by reading `down_revision` values (expected single head = the new id); (b) write a small temporary script that builds a temp SQLite file DB containing `categories(id, name, slug)` with rows including NULL slug, duplicate names after slugify ("Home & Living" vs "Home Living"), and an existing slug, imports the migration module, runs `upgrade()` under `alembic.migration.MigrationContext` + `alembic.operations.Operations.context(...)` bound to that temp DB, and asserts all slugs are non-null and unique; delete the temp script and DB afterwards. Do not use `.env` or the real DB URI.

- [ ] 4. Add and fix tests in `tests/test_product.py`.
      Depends on items 1 and 2. Keep the existing tests, but fix `test_create_real_product` to use the fixture's real category: look it up via `app` fixture (`with app.app_context(): Category.query.filter_by(name="Electronics").first().id`) or simply use `category_id: 1`; add `app` param and the `Category` import from `models` as needed. New tests (each creates its own uniquely named categories/products inside `app.app_context()` using `utils.db`, committing, so they do not disturb other tests, since fixtures are module-scoped and shared):
      - `test_filter_by_category_id`: create categories "TV" and "Audio" with a product each; `GET /products/?category_id=<tv id>` returns 200, only the TV product, and every item has `category_id == tv id`.
      - `test_filter_by_category_slug_and_name_case_insensitive`: `?category=tv`, `?category=TV`, and `?category=Tv` all return only the TV product (slug is auto-set to "tv" by `Category.__init__`); also test a multi-word name such as "Home Appliances" via `?category=home appliances` and via slug `?category=home-appliances`.
      - `test_invalid_category_id_returns_400`: `?category_id=abc` returns 400 with an `error` key.
      - `test_deleted_category_excluded`: soft-delete a category (`is_deleted = True`, commit); `?category_id=<id>` and `?category=<slug>` return `[]`, and the product is absent from the unfiltered `GET /products/`.
      - `test_null_category_product_still_listed`: product with `category_id=None` appears in unfiltered list.
      - `test_unknown_category_returns_empty_list`: `?category=nope` returns 200 and `[]`.
      - `test_create_product_invalid_category`: POST with nonexistent id returns 404, with a deleted category id returns 404, with `category_id: "abc"` returns 400; none creates a row.
      - `test_update_product_invalid_category`: PUT existing product with nonexistent/deleted category returns 404 and category unchanged; PUT with a valid category succeeds (200).
      - `test_is_sale_and_q_still_work`: regression for `?is_sale=true` and `?q=` combined with `?category_id=`.
      Use unique SKUs per test. Follow the existing style (plain functions, `client` fixture, `response.get_json()`).
      Files: tests/test_product.py
      Verify: `venv\Scripts\python.exe -m pytest tests -q` — all tests pass, including the pre-existing two.

- [ ] 5. Final full check.
      Run `venv\Scripts\python.exe -m pytest tests -q` once more and confirm green; run `git status` and confirm only `routes/product_routes.py`, `tests/test_product.py`, the new migration file (and `.agents/` artifacts) changed, and no seed file is modified. Clean any temporary files from item 3.
      Verify: pytest green; `git status` shows no seed file changes.

## Notes for the final summary
- Frontend should call `/products/?category=<slug>` or `/products/?category_id=<id>`. Existing categories with NULL slug need the migration applied by the user (`flask db upgrade`) for slug filtering; name-based filtering works immediately.
- Not addressed (out of scope): inconsistent seed data, missing `categories.image` migration, unnamed unique constraint in 9374b8d259f0 downgrade, PostgreSQL sequence reset.
