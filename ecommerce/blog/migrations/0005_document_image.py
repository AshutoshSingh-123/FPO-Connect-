# Generated by Django 3.0.7 on 2020-10-12 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201012_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='image',
            field=models.ImageField(null=True, upload_to='knowledge_image'),
        ),
    ]
