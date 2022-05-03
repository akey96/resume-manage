# Generated by Django 4.0.4 on 2022-04-22 14:52

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
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de Modificacion')),
                ('delete_date', models.DateField(auto_now=True, verbose_name='Fecha de Eliminacion')),
                ('rol', models.IntegerField(choices=[(0, 'None'), (1, 'Dev-Backend'), (2, 'Dev-Frontend'), (3, 'Devops'), (3, 'QA')], default=0, verbose_name='Roles')),
                ('first_name', models.CharField(max_length=255, verbose_name='Nombres')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Apellidos')),
                ('description', models.CharField(max_length=50, verbose_name='Description de Usuario')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Correo Electrónico')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='Telefono')),
                ('git', models.CharField(blank=True, max_length=255, verbose_name='github')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
    ]