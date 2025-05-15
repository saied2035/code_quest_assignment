from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0002_enable_pg_trgm_and_unaccent'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE INDEX product_name_trgm_idx
                ON product_product
                USING GIN (name gin_trgm_ops);
            """,
            reverse_sql="DROP INDEX product_name_trgm_idx;",
        ),
    ]
