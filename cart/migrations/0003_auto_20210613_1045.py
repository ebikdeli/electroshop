# Generated by Django 3.1.9 on 2021-06-13 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20210613_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_number',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
