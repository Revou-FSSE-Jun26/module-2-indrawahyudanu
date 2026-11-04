"""backfill category slugs
Revision ID: a1c4e7d29b53
Revises: 9374b8d259f0
Create Date: 2026-11-03 10:00:00.000000
"""
import re
import unicodedata

from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision = 'a1c4e7d29b53'
down_revision = '9374b8d259f0'
branch_labels = None
depends_on = None

SLUG_MAX = 120


def _slugify(text):
    text = unicodedata.normalize('NFKD', text or '').encode('ascii', 'ignore').decode('ascii').lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')


def upgrade():
    # Data-only: isi slug dari name untuk kategori lama yang slug-nya NULL/kosong
    categories = sa.table(
        'categories',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('slug', sa.String),
    )
    bind = op.get_bind()

    taken = set()
    for (slug,) in bind.execute(sa.select(categories.c.slug)):
        if slug:
            taken.add(slug.lower())

    rows = bind.execute(
        sa.select(categories.c.id, categories.c.name)
        .where(sa.or_(categories.c.slug.is_(None), categories.c.slug == ''))
        .order_by(categories.c.id)
    ).fetchall()

    for cat_id, name in rows:
        base = _slugify(name)[:SLUG_MAX] or f"category-{cat_id}"
        candidate = base
        if candidate in taken:
            suffix = f"-{cat_id}"
            candidate = base[:SLUG_MAX - len(suffix)].strip('-') + suffix
        taken.add(candidate)
        bind.execute(
            categories.update().where(categories.c.id == cat_id).values(slug=candidate)
        )


def downgrade():
    # No-op: backfill data tidak perlu dibatalkan
    pass
