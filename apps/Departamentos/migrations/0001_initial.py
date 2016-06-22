# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 16:53
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('fecha_ini', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(blank=True, choices=[('T', 'Tiempo completo'), ('P', 'Tiempo parcial'), ('', 'Sin especificar')], default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('NRC', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('fk_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Area')),
                ('fk_ciclo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Ciclo')),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nick', models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Use solo caracteres alfanumericos (a-Z, 0-9).')])),
                ('nombre', models.CharField(max_length=120)),
                ('jefeDep', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hora_ini', models.TimeField(blank=True, null=True)),
                ('hora_fin', models.TimeField(blank=True, null=True)),
                ('L', models.BooleanField(default=False)),
                ('M', models.BooleanField(default=False)),
                ('I', models.BooleanField(default=False)),
                ('J', models.BooleanField(default=False)),
                ('V', models.BooleanField(default=False)),
                ('S', models.BooleanField(default=False)),
                ('fk_aula', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Aula')),
                ('fk_edif', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Edificio')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('clave', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('fk_area', models.ManyToManyField(to='Departamentos.Area')),
                ('fk_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('codigo_udg', models.CharField(max_length=9, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Use solo caracteres numericos (0-9).')])),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.CharField(max_length=5, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Suplente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('periodo_ini', models.DateField(blank=True, null=True)),
                ('periodo_fin', models.DateField(blank=True, null=True)),
                ('fk_curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Curso')),
                ('fk_profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Profesor')),
            ],
        ),
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_horarios',
            field=models.ManyToManyField(blank=True, to='Departamentos.Horario'),
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Materia'),
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Profesor'),
        ),
        migrations.AddField(
            model_name='curso',
            name='fk_secc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Seccion'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='fk_curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Curso'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='fk_tipocont',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Departamentos.TipoContrato'),
        ),
        migrations.AddField(
            model_name='aula',
            name='fk_edif',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Edificio'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Departamento'),
        ),
    ]