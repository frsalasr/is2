# Generated by Django 2.0.1 on 2018-05-21 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0008_auto_20180521_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='preguntaclasificacion',
            name='numero_pregunta',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
