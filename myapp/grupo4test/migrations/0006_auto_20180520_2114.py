# Generated by Django 2.0.1 on 2018-05-21 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0005_auto_20180520_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formularioclasificacion',
            name='id_formulario',
        ),
        migrations.RemoveField(
            model_name='preguntaclasificacion',
            name='id_pregunta',
        ),
        migrations.AddField(
            model_name='formularioclasificacion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preguntaclasificacion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
