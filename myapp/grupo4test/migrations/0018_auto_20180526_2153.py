# Generated by Django 2.0.1 on 2018-05-27 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0017_remove_preguntaclasificacion_hijo_de'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntaclasificacion',
            name='depende_de',
            field=models.ManyToManyField(blank=True, null=True, related_name='_preguntaclasificacion_depende_de_+', to='grupo4test.PreguntaClasificacion'),
        ),
    ]
