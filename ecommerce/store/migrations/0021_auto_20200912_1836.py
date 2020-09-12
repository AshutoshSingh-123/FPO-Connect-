# Generated by Django 3.0.7 on 2020-09-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_product_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_unit',
            field=models.CharField(choices=[('Kg', 'Kg'), ('Liter', 'Liter'), ('Meter', 'Meter')], default=1, max_length=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.CharField(blank=True, choices=[('Dairy', 'Dairy'), ('Grain', 'Grain'), ('Fruit', 'Fruits')], max_length=6, null=True),
        ),
    ]
