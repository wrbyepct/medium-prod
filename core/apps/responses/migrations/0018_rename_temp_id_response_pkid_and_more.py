# Generated by Django 5.0.6 on 2025-01-03 06:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("responses", "0017_rename_pkid_response_id_rename_pkid_responseclap_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="response",
            old_name="temp_id",
            new_name="pkid",
        ),
        migrations.RenameField(
            model_name="responseclap",
            old_name="temp_id",
            new_name="pkid",
        ),
    ]
