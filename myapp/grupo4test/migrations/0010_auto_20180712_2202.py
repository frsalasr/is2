# Generated by Django 2.0.1 on 2018-07-12 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0009_auto_20180712_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formdiagnostico',
            name='estado',
            field=models.CharField(choices=[('ENVIADO', 'ENVIADO'), ('PENDIENTE', 'PENDIENTE'), ('VISTO', 'VISTO')], default='PENDIENTE', max_length=255),
        ),
    ]
