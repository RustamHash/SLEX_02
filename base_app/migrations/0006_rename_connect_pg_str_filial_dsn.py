# Generated by Django 5.0.4 on 2024-04-28 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0005_filial_connect_pg_str_filial_prog_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filial',
            old_name='connect_pg_str',
            new_name='dsn',
        ),
    ]