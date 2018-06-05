# Generated by Django 2.0.1 on 2018-05-29 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0023_auto_20180529_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='formularioclasificacion',
            name='comentario',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AddField(
            model_name='respuestasclasificacion',
            name='comentario',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='etapa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='preguntaclasificacion',
            name='numero_pregunta',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
