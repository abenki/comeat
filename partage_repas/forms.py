from django import forms
from .models import Repas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from .models import Repas,Comment

class RepasForm(forms.ModelForm):
    class Meta:
        model = Repas
        fields = 'menu','date','description', 'moyen_de_contact','nombre_participant','regime','allergene','prix'

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2')

class Changer_mdpForm(forms.Form):
        password=forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
        confirmation=forms.CharField(label="Confirmation", widget=forms.PasswordInput)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'commentaire',
