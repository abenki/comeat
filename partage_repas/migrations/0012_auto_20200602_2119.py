# Generated by Django 3.0.4 on 2020-06-02 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partage_repas', '0011_auto_20200602_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repas',
            name='participants',
        ),
        migrations.AddField(
            model_name='profil',
            name='mesrepas',
            field=models.ManyToManyField(to='partage_repas.Repas'),
        ),
    ]