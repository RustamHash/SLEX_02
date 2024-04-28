# Generated by Django 5.0.4 on 2024-04-28 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('position', models.IntegerField(default=0)),
                ('as_active', models.BooleanField(default=True)),
                ('filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='base_app.filial')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
                'ordering': ('position',),
            },
        ),
    ]
