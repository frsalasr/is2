# Generated by Django 2.0.6 on 2018-07-12 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0008_auto_20180712_0330'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tiempos',
            options={'ordering': ['-fecha_guardado']},
        ),
        migrations.AddField(
            model_name='cliente',
            name='nombre_empresa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]