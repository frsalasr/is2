# Generated by Django 2.0.1 on 2018-05-22 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grupo4test', '0010_auto_20180521_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='autor',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
