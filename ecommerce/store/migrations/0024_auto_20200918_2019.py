# Generated by Django 3.0.7 on 2020-09-18 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_fpo_registeration_fpo_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fpo_registeration',
            name='fpo_category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
