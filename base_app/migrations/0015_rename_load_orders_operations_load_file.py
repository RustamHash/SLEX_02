# Generated by Django 5.0.4 on 2024-04-30 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0014_rename_load_stock_pg_operations_load_stock_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operations',
            old_name='load_orders',
            new_name='load_file',
        ),
    ]
