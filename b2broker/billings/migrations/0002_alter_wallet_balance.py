# Generated by Django 5.0.4 on 2024-09-01 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=18, default='0', max_digits=30, verbose_name='Balance'),
        ),
    ]
