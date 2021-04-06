# Generated by Django 3.0.4 on 2020-06-03 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partage_repas', '0016_repas_dejainscrit'),
    ]

    operations = [
        migrations.AddField(
            model_name='repas',
            name='moyen_de_contact',
            field=models.TextField(default='', help_text="Ce ne sera visible que quand la personne s'inscrit au repas", verbose_name='Comment me contacter'),
        ),
        migrations.AlterField(
            model_name='repas',
            name='nombre_participant',
            field=models.PositiveIntegerField(),
        ),
    ]