# Generated by Django 5.1.2 on 2025-04-15 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_customer_state_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatus',
            name='order_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
