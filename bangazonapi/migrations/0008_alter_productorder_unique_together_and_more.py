# Generated by Django 4.1.3 on 2023-01-17 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bangazonapi', '0007_rename_quantity_product_inventory'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productorder',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in-progress', 'In Progress'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='in-progress', max_length=20),
        ),
    ]
