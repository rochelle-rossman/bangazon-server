# Generated by Django 4.1.3 on 2023-01-16 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bangazonapi', '0006_alter_productorder_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantity',
            new_name='inventory',
        ),
    ]
