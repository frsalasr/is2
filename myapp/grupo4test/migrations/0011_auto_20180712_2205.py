# Generated by Django 2.0.1 on 2018-07-12 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0010_auto_20180712_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formdiagnostico',
            name='estado',
            field=models.CharField(choices=[('NUEVO', 'NUEVO'), ('ENVIADO', 'ENVIADO'), ('PENDIENTE', 'PENDIENTE'), ('VISTO', 'VISTO')], default='NUEVO', max_length=255),
        ),
    ]
