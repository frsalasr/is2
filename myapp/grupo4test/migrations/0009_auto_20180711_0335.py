# Generated by Django 2.0.6 on 2018-07-11 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0008_auto_20180711_0314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formdiagnostico',
            old_name='Q',
            new_name='dimension',
        ),
    ]
