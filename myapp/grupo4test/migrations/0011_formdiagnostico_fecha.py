# Generated by Django 2.0.6 on 2018-07-01 18:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0010_formdiagnostico_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdiagnostico',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]