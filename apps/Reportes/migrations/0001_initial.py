# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 16:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Departamentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('horasFalta', models.IntegerField()),
                ('comentario', models.CharField(blank=True, max_length=100)),
                ('fk_contrato', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Contrato')),
                ('fk_depto', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='Departamentos.Departamento')),
            ],
        ),
    ]