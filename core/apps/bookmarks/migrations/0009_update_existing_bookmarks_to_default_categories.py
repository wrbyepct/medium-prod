from django.db import migrations


def create_default_category(apps, schema_editor):
    User = apps.get_model("user", "User")
    ReadingCategory = apps.get_model("bookmarks", "ReadingCategory")

    for user in User.objects.all():
        ReadingCategory.objects.create(user=user, title="Reading list")


def update_existing_bookmark_to_default_categories(apps, schema_editor):
    ReadingCategory = apps.get_model("bookmarks", "ReadingCategory")
    User = apps.get_model("user", "User")

    for user in User.objects.all():
        reading_list = ReadingCategory.objects.get(user=user, title="Reading list")
        reading_list.bookmarks.set(user.bookmarks.all())


class Migration(migrations.Migration):
    dependencies = [("bookmarks", "0008_alter_bookmarksincategories_category")]
    operations = [
        migrations.RunPython(create_default_category),
        migrations.RunPython(update_existing_bookmark_to_default_categories),
    ]
