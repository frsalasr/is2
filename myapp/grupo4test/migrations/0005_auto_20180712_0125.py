# Generated by Django 2.0.6 on 2018-07-12 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0004_auto_20180711_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestadiagnostico',
            name='respuesta_alternativa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='grupo4test.TipoAlternativa'),
        ),
        migrations.AddField(
            model_name='respuestadiagnostico',
            name='respuestas_eleccion',
            field=models.ManyToManyField(blank=True, null=True, to='grupo4test.TipoElegir'),
        ),
    ]