# Generated by Django 5.0.4 on 2024-05-02 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0016_alter_operations_options_contracts_operation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracts',
            name='operation',
        ),
    ]
