# Generated by Django 3.1.9 on 2021-06-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_activity', '0003_auto_20210629_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, max_length=1500),
        ),
    ]
