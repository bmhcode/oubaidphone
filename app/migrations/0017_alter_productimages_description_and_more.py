# Generated by Django 5.0 on 2024-02-11 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='description',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Description'),
        ),
        migrations.DeleteModel(
            name='ProductsRelated',
        ),
    ]
