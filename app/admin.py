from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import *

class CustomUserAdmin(UserAdmin):
    # Les champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'nom', 'tel',  'is_staff')
    
    # Les champs par lesquels on peut filtrer
    list_filter = ( 'is_staff', 'is_superuser')
    
    # Les champs à afficher dans le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('nom', 'email', 'tel')
        }),
        
        ('Permissions', {
            'fields': ('is_active',  'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Les champs à afficher dans le formulaire de création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nom', 'tel',  'password1', 'password2'),
        }),
    )
    
    # Recherche par ces champs
    search_fields = ('username', 'email', 'nom', 'tel')
    
    # Tri par défaut
    ordering = ('username',)
admin.site.register(Utilisateur, CustomUserAdmin)
admin.site.register(Client)
admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(Commande)
admin.site.register(Notification)
# Register your models here.
