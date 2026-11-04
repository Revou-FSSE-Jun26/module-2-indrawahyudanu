# Category filter and validation for products

Product listing ignored any category parameter, so opening the TV category returned every product. The commit adds `category_id` and `category` (slug or name) filters to `GET /products/`. It also validates `category_id` on create and update, and adds a data-only Alembic migration that backfills NULL or empty category slugs. This was reviewed as commit 6d7b172, because the fix is already committed and the working tree only holds an unrelated `models.py` edit.

Watch for: (1) listing now hides products whose category is soft-deleted, a behavior change beyond the filter (confirmed); (2) the uncommitted `models.py` edit gives a String `description` column `server_default='False'` and has no migration (confirmed, not part of this commit).

**Verdict**: APPROVED

## High-level view

The list query now outer-joins categories. Products with no category still appear, and products in a soft-deleted category are hidden. The `category_id` filter returns 400 on a non-integer value. The `category` filter matches slug or name case-insensitively. The `is_sale`, `q` and response shape code is unchanged in the diff.

Create and update share a `_check_category` helper that rejects non-integers and booleans (400) and missing or deleted categories (404). Validation only runs when `category_id` is present and not null, so creating a product without a category still works.

The migration is data-only. It fills missing slugs from the category name, de-duplicates by appending the id, and has a no-op downgrade. It chains from `9374b8d259f0`, and the chain is linear, so `a1c4e7d29b53` is the single head. The verification doc shows 11 tests passing and a throwaway-SQLite migration run. Seed files and `.env` are not in the commit.

<details>
<summary>Issues (3)</summary>

1. **Soft-deleted category hides products (confirmed)**: the base list query now excludes products whose category is deleted, even without a category filter. Non-blocking and plausibly intended. Confirm with the owner and mention it in the PR notes.
2. **Backfill suffix collision (possible)**: the fallback `base-<id>` is added to `taken` but never re-checked against it. It could collide with an existing slug such as `tv-4`. Very unlikely, and only matters if slug has a unique constraint. Loop until the candidate is free if you want to be safe.
3. **Uncommitted `description` column (confirmed, out of scope)**: the working-tree `models.py` adds a String column with `server_default='False'` and no migration. Fix the default and add a migration before committing it.

</details>

<details>
<summary>Details</summary>

### Listing query and the soft-delete side effect

```
Product LEFT JOIN Category
  WHERE product.is_deleted = false
    AND (product.category_id IS NULL OR category.is_deleted = false)
  [+ is_sale] [+ category_id] [+ category slug/name] [+ q]
```

Uncategorised products stay visible, which keeps the old behavior for them. The new `OR` clause also drops products in a soft-deleted category from the unfiltered listing. That is a visible change for existing data, so it should be a conscious decision.

### Migration slug backfill

The `taken` set is seeded with existing slugs in lowercase, so reruns and partial data are safe. A collision is resolved by appending `-<id>`. That suffixed candidate is not re-checked against `taken`, hence issue 2. The upgrade changes data only, and the downgrade is a deliberate no-op.

### Not tested

The migration was never run against the user's database. The evidence is a throwaway SQLite run only. I did not re-run the tests or the build, per instructions, and I did not read the test file line by line. I relied on the recorded results, which show 2 existing tests adjusted and 9 new ones.

</details>

<details>
<summary>File map</summary>

- `routes/product_routes.py`: category filters, `_check_category`, validation in create and update
- `migrations/versions/a1c4e7d29b53_backfill_category_slugs.py`: new data-only slug backfill
- `tests/test_product.py`: create test uses `category_id: 1`, plus new filter and validation tests

Full diff: `git show 6d7b172`

</details>
