# Generated by Django 5.0.4 on 2024-04-30 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0013_alter_operations_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operations',
            old_name='load_stock_pg',
            new_name='load_stock',
        ),
        migrations.RemoveField(
            model_name='operations',
            name='load_stock_wms',
        ),
    ]