# Generated by Django 3.0.7 on 2020-10-12 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_document_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='link',
            field=models.URLField(null=True),
        ),
    ]
