# Generated by Django 2.0.6 on 2018-06-17 02:35

from django.db import migrations, models
import grupo4test.models


class Migration(migrations.Migration):

    dependencies = [
        ('grupo4test', '0004_document_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=grupo4test.models.Document.get_upload_path),
        ),
    ]