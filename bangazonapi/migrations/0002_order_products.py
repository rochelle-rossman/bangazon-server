# Generated by Django 4.1.3 on 2023-01-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bangazonapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='bangazonapi.ProductOrder', to='bangazonapi.product'),
        ),
    ]
