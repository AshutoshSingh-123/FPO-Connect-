# Generated by Django 3.0.7 on 2020-10-17 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
