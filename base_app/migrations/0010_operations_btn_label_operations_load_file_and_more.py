# Generated by Django 5.0.4 on 2024-04-30 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0009_operations'),
    ]

    operations = [
        migrations.AddField(
            model_name='operations',
            name='btn_label',
            field=models.CharField(default=1, max_length=155),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operations',
            name='load_file',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='operations',
            name='search_goods',
            field=models.BooleanField(default=True),
        ),
    ]