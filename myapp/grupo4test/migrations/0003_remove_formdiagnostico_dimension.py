# Generated by Django 2.0.1 on 2018-07-11 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0002_auto_20180711_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdiagnostico',
            name='dimension',
        ),
    ]
