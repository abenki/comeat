# Generated by Django 3.0.4 on 2020-06-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partage_repas', '0005_auto_20200601_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repas',
            name='nombre_d_inscrit',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='repas',
            name='nombre_participant',
            field=models.IntegerField(null=True),
        ),
    ]
