# Generated by Django 3.0.4 on 2020-06-05 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partage_repas', '0026_auto_20200605_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repas',
            name='regime',
            field=models.CharField(choices=[('Classique', 'Classique'), ('Halal', 'Halal'), ('Végétarien', 'Végétarien'), ('Végétalien', 'Végétalien'), ('Sans Gluten,', 'GlutenFree')], default='Classique', max_length=100),
        ),
    ]
