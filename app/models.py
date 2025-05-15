from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UtilisateurManager(BaseUserManager):
    def create_user(self,  username, password=None, **extra_fields):
        # if not email:
        #     raise ValueError('Users must have an email address')
        # email = self.normalize_email(email)
        user = self.model( username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user( username, password, **extra_fields)

class Utilisateur(AbstractUser):
    nom = models.CharField(_('full name'), max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    tel = models.CharField(_('phone number'), max_length=20)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nom', 'tel']

    objects = UtilisateurManager()

    def __str__(self):
        return self.username or self.tel

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Client(Utilisateur):
    class Meta:
        proxy = False

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def rechercher_produits(self):
        from .models import Produit
        return Produit.objects.filter(disponible=True)

    def commander_produit(self, produit, quantite):
        from .models import Commande
        return Commande.objects.create(client=self, produit=produit, quantite=quantite)

class Fournisseur(Utilisateur):
    def ajouter_produit(self, produit):
        produit.fournisseur = self
        produit.save()

    def consulter_commandes(self):
        from .models import Commande
        return Commande.objects.filter(produit__fournisseur=self)

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.nom

class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    quantite_stock = models.PositiveIntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom

class Commande(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('canceled', 'Annulée'),
        ('delivered', 'Livrée'),
    ]
    
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.CASCADE,
        related_name='commandes'
    )
    quantite = models.PositiveIntegerField(default=1)
    date_commande = models.DateTimeField(auto_now_add=True)
    date_livraison = models.DateField(null=True, blank=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=50, default='pending', choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.client.email} - {self.produit.nom}"

    def confirmer(self):
        self.statut = 'confirmed'
        self.save()
        Notification.objects.create(
            user=self.client,
            message=f"Votre commande pour {self.produit.nom} a été confirmée",
            commande=self
        )

    def annuler(self):
        self.statut = 'canceled'
        self.save()
        Notification.objects.create(
            user=self.client,
            message=f"Votre commande pour {self.produit.nom} a été annulée",
            commande=self
        )

    def save(self, *args, **kwargs):
        if not self.montant_total and self.produit and self.quantite:
            self.montant_total = self.produit.prix * self.quantite
        super().save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification pour {self.user.username}"