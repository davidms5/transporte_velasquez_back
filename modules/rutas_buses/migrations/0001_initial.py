# Generated by Django 5.1.6 on 2025-02-17 02:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_id', models.CharField(max_length=10, unique=True)),
                ('modelo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Conductor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('numero_licencia', models.CharField(max_length=20, unique=True)),
                ('dpi', models.CharField(max_length=20, unique=True)),
                ('expiracion_licencia', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origen', models.CharField(max_length=100)),
                ('destino', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bus', models.ManyToManyField(related_name='rutas', to='rutas_buses.bus')),
                ('conductor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rutas_buses.conductor')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='ruta_asignada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buses', to='rutas_buses.ruta'),
        ),
    ]
