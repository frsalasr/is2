# Generated by Django 2.0.6 on 2018-07-01 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0009_auto_20180629_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdiagnostico',
            name='estado',
            field=models.CharField(choices=[('RESUELTO', 'RESUELTO'), ('PENDIENTE', 'PENDIENTE'), ('CORREGIR', 'CORREGIR')], default='PENDIENTE', max_length=512),
        ),
    ]