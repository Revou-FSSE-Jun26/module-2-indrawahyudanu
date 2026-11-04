# Verification: category filter fix

Run from `c:\Users\ASUS\Documents\File danu\revoshop-db`.

| Command | Result |
|---|---|
| `venv\Scripts\python.exe -m py_compile routes\product_routes.py tests\test_product.py migrations\versions\a1c4e7d29b53_backfill_category_slugs.py` | exit 0 |
| `venv\Scripts\python.exe -m pytest -q` | 11 passed, 13 warnings (utcnow / Query.get deprecations, pre-existing) |
| Temporary script (deleted afterwards) running the migration `upgrade()` + `downgrade()` on a throwaway SQLite file in the temp dir | OK: rows `Home & Living`->`home-living`, `Home Living`->`home-living-2`, `tv` (NULL slug, existing `tv`)->`tv-4`, `!!!`->`category-6`, existing slug kept; all non-null and unique |

## Notes
- Migration `a1c4e7d29b53` has `down_revision = '9374b8d259f0'`; all `down_revision` values read, so it is the single head. NOT run against the user's DB. `.env` not read.
- `slugify` is in `utils.py`, not `models.py`, so the migration inlines an equivalent (lowercase, non-alphanumerics to `-`, trim `-`).
- Tests: 2 existing (create fixed to `category_id: 1`, since id 2 no longer exists and is now rejected) + 9 new.
- Seed files untouched. `models.py` had a pre-existing uncommitted change; not part of this commit.
