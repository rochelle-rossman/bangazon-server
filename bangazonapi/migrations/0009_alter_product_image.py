# Generated by Django 4.1.5 on 2023-01-18 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bangazonapi', '0008_alter_productorder_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
