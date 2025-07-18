# Generated by Django 5.2.3 on 2025-07-07 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanque',
            name='amonia',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tanque',
            name='dureza_carbonatos',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tanque',
            name='dureza_geral',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tanque',
            name='nitrato',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tanque',
            name='nitrito',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tanque',
            name='salinidade',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tanque',
            name='tds',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
