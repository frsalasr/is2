# Generated by Django 2.0.6 on 2018-06-16 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrpcion', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ejemplo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('rut', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('etapa', models.CharField(blank=True, max_length=255, null=True)),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FormDiagnostico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.FloatField(blank=True, default=0, null=True)),
                ('respondido', models.BooleanField(default=False)),
                ('validado', models.BooleanField(default=False)),
                ('editable', models.BooleanField(default=False)),
                ('comentario', models.CharField(blank=True, default='', max_length=512)),
                ('Q', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('empresa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='grupo4test.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable1', models.IntegerField()),
                ('variable2', models.IntegerField()),
                ('variable3', models.IntegerField()),
                ('variable_hid', models.IntegerField(blank=True, null=True)),
                ('result', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormularioClasificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.FloatField(blank=True, null=True)),
                ('respondido', models.BooleanField(default=False)),
                ('validado', models.BooleanField(default=False)),
                ('comentario', models.CharField(blank=True, default='', max_length=512)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupo4test.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Postulante',
            fields=[
                ('run', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('nombre_empresa', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('webpage', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaClasificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_pregunta', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('ponderacion', models.IntegerField()),
                ('texto_pregunta', models.CharField(max_length=255)),
                ('tipo_pregunta', models.CharField(blank=True, choices=[('a', 'Alternativa'), ('n', 'Número'), ('t', 'Texto')], default='a', max_length=1, null=True)),
                ('base_question', models.BooleanField(default=False)),
                ('depende_de', models.ManyToManyField(blank=True, related_name='_preguntaclasificacion_depende_de_+', to='grupo4test.PreguntaClasificacion')),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaDiagnostico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('sub_numero', models.IntegerField(blank=True, null=True)),
                ('Q', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('ponderacion', models.IntegerField(default=1)),
                ('texto_pregunta', models.CharField(max_length=255)),
                ('tipo_pregunta', models.CharField(blank=True, choices=[('a', 'Alternativa'), ('n', 'Número'), ('t', 'Texto')], default='a', max_length=1, null=True)),
                ('base_question', models.BooleanField(default=False)),
                ('Document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='grupo4test.Document')),
                ('depende_de', models.ManyToManyField(blank=True, related_name='_preguntadiagnostico_depende_de_+', to='grupo4test.PreguntaDiagnostico')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaDiagnostico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField()),
                ('respuesta', models.CharField(blank=True, max_length=255)),
                ('comentario', models.CharField(blank=True, default='', max_length=255)),
                ('formulario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupo4test.FormDiagnostico')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupo4test.PreguntaDiagnostico')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestasClasificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje', models.IntegerField()),
                ('respuesta', models.CharField(blank=True, max_length=255)),
                ('comentario', models.CharField(blank=True, default='', max_length=255)),
                ('formulario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupo4test.FormularioClasificacion')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupo4test.PreguntaClasificacion')),
            ],
        ),
        migrations.CreateModel(
            name='TipoAlternativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_alternativa', models.CharField(max_length=255)),
                ('puntaje', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoElegir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_eleccion', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='preguntadiagnostico',
            name='preguntas_alternativa',
            field=models.ManyToManyField(blank=True, to='grupo4test.TipoAlternativa'),
        ),
        migrations.AddField(
            model_name='preguntaclasificacion',
            name='preguntas_alternativa',
            field=models.ManyToManyField(blank=True, to='grupo4test.TipoAlternativa'),
        ),
        migrations.AddField(
            model_name='formularioclasificacion',
            name='preguntas',
            field=models.ManyToManyField(through='grupo4test.RespuestasClasificacion', to='grupo4test.PreguntaClasificacion'),
        ),
        migrations.AddField(
            model_name='formulario',
            name='postulante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupo4test.Postulante'),
        ),
        migrations.AddField(
            model_name='formdiagnostico',
            name='preguntas',
            field=models.ManyToManyField(through='grupo4test.RespuestaDiagnostico', to='grupo4test.PreguntaDiagnostico'),
        ),
    ]
