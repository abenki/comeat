from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator
import pytz
from decimal import *
from django.conf import settings

# Create your models here.

class Repas(models.Model):
    menu = models.CharField(max_length=100)
    date = models.DateTimeField(verbose_name="Date et heure du repas",help_text="jj/mm/aaaa hh:mm")
    utilisateur = models.CharField(null=True,max_length=100)
    description = models.TextField(null=True)
    moyen_de_contact=models.TextField(verbose_name="Comment me contacter",help_text="Ce champ sera visible uniquement par les personnes inscrites au repas",default="")
    nombre_participant = models.PositiveIntegerField(verbose_name="Nombre maximal de participants", null=False)
    nombre_d_inscrit = models.PositiveIntegerField(null=True,default=0)
    prix=models.DecimalField(verbose_name="Prix de participation", max_digits=5, decimal_places=2, default=5, validators=[MinValueValidator(Decimal('0.01'))])
    regime=models.CharField(verbose_name="Régime alimentaire", default='Classique',choices=[('Classique','Classique'),('Halal','Halal'),('Végétarien','Végétarien'),('Végétalien','Végétalien'),('Sans Gluten','Sans Gluten')],max_length=100)
    allergene=models.CharField(verbose_name="Allergènes", default='Aucun',max_length=100,help_text='Les allergènes courants sont le lait, les oeufs, les crustacées, les noix')

    class Meta:
        verbose_name = "repas"
        ordering = ['date']

    def place_restantes(self):
        return max((self.nombre_participant - self.nombre_d_inscrit),0)

    def est_dans_futur(self):
        return(self.date >= pytz.utc.localize(datetime.utcnow()))

    def reserver(self,pk, *args, **kwargs):
        if self.place_restantes() > 0 :
            self.nombre_d_inscrit += 1
            super().save(*args, **kwargs)
            return True
        else:
            return False

    def desinscrire(self, *args, **kwargs):
        if self.nombre_d_inscrit > 0:
            self.nombre_d_inscrit -= 1
            super().save(*args, **kwargs)

    def supprimer(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.menu

class Comment(models.Model):
    post = models.ForeignKey('partage_repas.Repas', on_delete=models.CASCADE, related_name='comments')
    pseudo = models.ForeignKey(User,on_delete=models.CASCADE,db_column='pseudo')
    commentaire = models.TextField(verbose_name="")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.commentaire

class Inscrit(models.Model):
    nom=models.CharField(max_length=100)
    idrepas=models.PositiveIntegerField(null=True)

    def supprimer(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.nom

class Boolean(models.Model):
    nom=models.CharField(max_length=100)
    valeur=models.BooleanField()

    def rend_vrai(self, *args, **kwargs):
        self.valeur=True
        super().save(*args, **kwargs)
        return self.nom

    def rend_faux(self, *args, **kwargs):
        self.valeur=False
        super().save(*args, **kwargs)
        return self.nom

    def est_faux(self):
        return self.valeur == False

    def __str__(self):
        return self.nom
