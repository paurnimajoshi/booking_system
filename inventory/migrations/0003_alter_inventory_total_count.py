# Generated by Django 4.2.19 on 2025-02-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventory_description_inventory_expiration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='total_count',
            field=models.IntegerField(default=0),
        ),
    ]
