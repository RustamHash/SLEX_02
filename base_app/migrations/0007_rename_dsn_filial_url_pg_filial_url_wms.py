# Generated by Django 5.0.4 on 2024-04-29 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0006_rename_connect_pg_str_filial_dsn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filial',
            old_name='dsn',
            new_name='url_pg',
        ),
        migrations.AddField(
            model_name='filial',
            name='url_wms',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
