from django.shortcuts import render
from django.http import HttpResponse
from .forms import RepasForm, InscriptionForm, ConnexionForm, Changer_mdpForm, CommentForm
from django.shortcuts import redirect
from .models import Repas, Inscrit,Boolean,Comment
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

# Create your views here.

def creer_repas(request):
    if request.method == "POST" :
        form = RepasForm(request.POST)
        if form.is_valid():
            repas = form.save(commit=False)
            repas.utilisateur = request.user.username
            repas.save()
            return redirect('listerepas')
        else:
            messages.error(request,'Le formulaire n\'a pas été rempli correctement')
    else:
        form=RepasForm()
    return render(request, 'partage_repas/repasform.html', locals())

def repas_details(request,pk):
    repas=Repas.objects.get(pk=pk)
    comments=Comment.objects.all()
    utilisateurs= User.objects.all()
    inscrit = Inscrit.objects.all()
    b=Boolean.objects.create(nom='',valeur=False)

    context = {'comments':comments,
                'utilisateurs':utilisateurs,
                'inscrit':inscrit,
                'b':b,
                'repas':repas}
    return render(request, 'partage_repas/repas_details.html', context)

def profil_details(request,pk):
    repas=Repas.objects.all()
    utilisateurs= User.objects.all()
    inscrit = Inscrit.objects.all()
    repas_=Repas.objects.get(pk=pk)
    profil=User.objects.get(username=repas_.utilisateur)
    b=Boolean.objects.create(nom='',valeur=False)
    context = {'repas':repas,
                'utilisateurs':utilisateurs,
                'inscrit':inscrit,
                'b':b,
                'profil':profil}
    return render(request, 'partage_repas/profil_details.html', context)

def laisser_commentaire(request, pk):
    post = Repas.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.pseudo=request.user
            comment.save()
            return redirect('repas_details', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'partage_repas/laisser_commentaire.html', {'form': form})

def mesrepas (request):
    repas = Repas.objects.all()
    inscrit = Inscrit.objects.all()
    return render(request, 'partage_repas/mesrepas.html', locals())

def listerepas(request, page=1):
    repaslist= Repas.objects.all()
    utilisateurs= User.objects.all()
    inscrit = Inscrit.objects.all()
    b=Boolean.objects.create(nom='',valeur=False)
    paginator = Paginator(repaslist, 5)
    try:
        repas = paginator.page(page)
    except EmptyPage:
        repas = paginator.page(paginator.num_pages)

    context = {'repaslist':repaslist,
                'utilisateurs':utilisateurs,
                'inscrit':inscrit,
                'b':b,
                'paginator':paginator,
                'repas':repas}
    return render(request, 'partage_repas/listerepas.html', context)

def reserver_repas (request, pk):
    if request.method == 'POST':
        rep=Repas.objects.get(pk=pk)
        if rep.reserver(pk):
            Inscrit.objects.create(nom=request.user.username, idrepas=pk)
        else:
            messages.error(request,'Impossible complet')
    repas = Repas.objects.all()
    inscrit = Inscrit.objects.all()
    return render(request, 'partage_repas/mesrepas.html', locals())

def supprimer_repas (request, pk):
    if request.method == 'POST':
        rep=Repas.objects.get(pk=pk)
        rep.supprimer()
    repas = Repas.objects.all()
    inscrit = Inscrit.objects.all()
    return render(request, 'partage_repas/mesrepas.html', locals())

def desinscrire_repas (request, pk):
    if request.method == 'POST':
        ins=Inscrit.objects.get(nom=request.user.username,idrepas=pk)
        rep=Repas.objects.get(pk=pk)
        if ins != None:
            ins.supprimer()
            rep.desinscrire()
        else:
            messages.error(request,'Impossible vous n\'etiez pas inscrit')
    repas = Repas.objects.all()
    inscrit = Inscrit.objects.all()
    return render(request, 'partage_repas/mesrepas.html', locals())

def connexion(request):
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
                messages.error(request,'Le nom d\'utilisateur et le mot de passe ne correspondent pas')
                return render(request, 'partage_repas/connexion.html',locals())
        if  request.user.is_authenticated:
            return render(request, 'partage_repas/profil.html', locals())
        else :
            messages.error(request,'Le nom d\'utilisateur et le mot de passe ne correspondent pas')
            return render(request, 'partage_repas/connexion.html',locals())
    form = ConnexionForm()
    return render(request, 'partage_repas/connexion.html', locals())


def profil(request):
    return render(request, 'partage_repas/profil.html', locals())

def changer_mdp(request):
    form= Changer_mdpForm(request.POST or None)
    envoie = True,
    if form.is_valid():
        password=form.cleaned_data["password"]
        confirmation=form.cleaned_data["confirmation"]
        if (password == confirmation and len(password)>=8):
            request.user.set_password(password)
            request.user.save()
            user = authenticate(username=request.user.username, password=password)
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
            return render(request, 'partage_repas/accueil.html', locals())
        else:
            error=True
            messages.error(request,'Erreur dans changement de mot de passe')
    return render(request, 'partage_repas/changer_mdp.html', locals())


def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'Le formulaire n\'a pas été rempli correctement')
    else:
        form = InscriptionForm()
    return render(request, 'partage_repas/inscriptionform.html', {'form': form})

def rechercher(request):
    query = request.GET.get('search')
    resultat = Repas.objects.filter(Q(menu__icontains=query) | Q(utilisateur__icontains=query) | Q(description__icontains=query) | Q(regime__icontains=query))
    b=Boolean.objects.create(nom='',valeur=False)
    return render(request, 'partage_repas/resultat_recherche.html', locals())


def accueil(request):
    return render(request, 'partage_repas/accueil.html')
