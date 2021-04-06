from django.test import TestCase
from datetime import datetime, timedelta
import pytz
from .models import Repas, Inscrit, Boolean, Comment

# Create your tests here.
#self.assertEqual/True/False/...(,)

class RepasTests(TestCase):
	def setUp(self):
		Repas.objects.create(menu="manger_futur", date=pytz.utc.localize(datetime.now() + timedelta(days=20)),nombre_participant=3)
		Repas.objects.create(menu="manger_passe", date=pytz.utc.localize(datetime.now() - timedelta(days=20)),nombre_participant=3)
		Repas.objects.create(menu="manger_inscrit", date=datetime.now(),nombre_participant=3,nombre_d_inscrit=5)
		Repas.objects.create(menu="manger_complet", date=datetime.now(),nombre_participant=3,nombre_d_inscrit=3)
		Repas.objects.create(menu="manger_vide", date=datetime.now(),nombre_participant=3,nombre_d_inscrit=0)
		Repas.objects.create(menu="manger_d_inscrit_2", date=datetime.now(),nombre_participant=3,nombre_d_inscrit=5)

	def test_est_dans_futur_fonctionnne(self):
		futur_repas=Repas.objects.get(menu="manger_futur")
		self.assertTrue(futur_repas.est_dans_futur())
		passe_repas=Repas.objects.get(menu="manger_passe")
		self.assertFalse(passe_repas.est_dans_futur())

	def test_inscription_impossible_si_plus_de_place(self):
		repas_complet=Repas.objects.get(menu="manger_complet")
		repas_vide=Repas.objects.get(menu="manger_vide")
		n=repas_vide.nombre_d_inscrit
		m=repas_complet.nombre_d_inscrit
		repas_vide.reserver(repas_vide.pk)
		repas_complet.reserver(repas_complet.pk)
		self.assertEqual(repas_vide.nombre_d_inscrit,n+1)
		self.assertEqual(repas_complet.nombre_d_inscrit,m)

	def test_desinscription_impossible_si_personne_inscrit(self):
		repas_complet=Repas.objects.get(menu="manger_complet")
		repas_vide=Repas.objects.get(menu="manger_vide")
		n=repas_vide.nombre_d_inscrit
		m=repas_complet.nombre_d_inscrit
		repas_vide.desinscrire()
		repas_complet.desinscrire()
		self.assertEqual(repas_vide.nombre_d_inscrit,n)
		self.assertEqual(repas_complet.nombre_d_inscrit,m-1)

class BooleanTest(TestCase):
	def setUp(self):
		true = Boolean.objects.create(nom='true',valeur=True)
		false = Boolean.objects.create(nom='false',valeur=False)

	def test_est_faux_fonctionne(self):
		true=Boolean.objects.get(nom='true')
		false=Boolean.objects.get(nom='false')
		self.assertEqual(false.est_faux(),True)
		self.assertEqual(true.est_faux(),False)