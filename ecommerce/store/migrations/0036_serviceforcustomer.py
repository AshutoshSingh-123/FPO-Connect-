# Generated by Django 3.0.7 on 2020-10-14 13:17

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0035_auto_20201008_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceForCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_unit', models.CharField(choices=[('Hrs.', 'Hrs.'), ('Netting', 'Netting'), ('Day', 'Day')], max_length=20)),
                ('service_price', models.FloatField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('service_description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('service_title', models.CharField(max_length=50)),
                ('service_by', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='store.Fpo_Registeration')),
                ('service_by1', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
