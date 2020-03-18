# Generated by Django 2.1.7 on 2020-03-17 21:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marcacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_usuario', models.CharField(max_length=40)),
                ('nome_usuario', models.CharField(max_length=100)),
                ('data_marcacao', models.DateTimeField(default=django.utils.timezone.now, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarcacoesPorDia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]