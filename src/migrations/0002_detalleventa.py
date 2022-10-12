# Generated by Django 3.1.7 on 2022-10-08 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalleventa',
            fields=[
                ('detalleventaid', models.BigIntegerField(primary_key=True, serialize=False)),
                ('cantidad', models.BigIntegerField()),
                ('subtotal', models.BigIntegerField()),
            ],
            options={
                'db_table': 'detalleventa',
                'managed': False,
            },
        ),
    ]
