from django.contrib import admin

# Register your models here.
from .models import Repas, Inscrit,Comment

admin.site.register(Repas)
admin.site.register(Comment)
admin.site.register(Inscrit)