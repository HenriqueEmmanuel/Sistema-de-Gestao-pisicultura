# Generated by Django 5.2.3 on 2025-07-23 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_usuario_alertas_agua_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='unidade_temperatura',
            new_name='temperatura',
        ),
    ]
