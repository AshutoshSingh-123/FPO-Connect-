# Generated by Django 3.0.7 on 2020-10-02 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0030_auto_20201001_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_by1',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
