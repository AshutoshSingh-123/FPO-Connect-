# Generated by Django 3.0.7 on 2020-10-17 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20201017_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]