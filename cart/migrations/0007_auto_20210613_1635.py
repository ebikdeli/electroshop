# Generated by Django 3.1.9 on 2021-06-13 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20210613_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.PositiveIntegerField(),
        ),
    ]
