# Generated by Django 4.1.3 on 2023-01-25 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bangazonapi', '0010_alter_product_product_type_alter_store_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bangazonapi.paymentmethod'),
        ),
    ]