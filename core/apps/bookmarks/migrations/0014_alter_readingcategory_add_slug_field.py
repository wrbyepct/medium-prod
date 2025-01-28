import hashlib

from autoslug import AutoSlugField
from django.db import migrations
from django.utils.text import slugify

from core.tools.hash import generate_hashed_slug as _


def generate_hashed_slug(apps, schema_editor):
    ReadingCategory = apps.get_model("bookmarks", "ReadingCategory")

    for bc in ReadingCategory.objects.all():
        base_slug = slugify(bc.title)
        unique_hash = hashlib.md5(str(bc).encode("utf-8")).hexdigest()[:13]  # noqa: S324
        bc.slug = f"{base_slug}-{unique_hash}"
        bc.save()


class Migration(migrations.Migration):
    dependencies = [
        ("bookmarks", "0013_alter_readingcategory_options"),
    ]
    operations = [
        migrations.AddField(
            model_name="ReadingCategory",
            name="slug",
            field=AutoSlugField(populate_from=_, always_update=True, null=True),
        ),
        migrations.RunPython(generate_hashed_slug),
    ]
