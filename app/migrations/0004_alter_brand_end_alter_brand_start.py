# Generated by Django 5.0 on 2023-12-15 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_brand_product_featured_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='end',
            field=models.DateTimeField(verbose_name='End at'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='start',
            field=models.DateTimeField(verbose_name='Start at'),
        ),
    ]
