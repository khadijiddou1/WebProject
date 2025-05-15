from rest_framework import serializers
from .models import Utilisateur, Client, Fournisseur, Categorie, Produit, Commande, Notification
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_client'] = isinstance(user, Client)
        token['is_fournisseur'] = isinstance(user, Fournisseur)
        return token

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'nom', 'tel']

class ClientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'nom', 'tel']
    
    def create(self, validated_data):
        user = Client.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nom=validated_data['nom'],
            tel=validated_data['tel']
        )
        return user

class FournisseurRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Fournisseur
        fields = ['username', 'email', 'password', 'nom', 'tel']
    
    def create(self, validated_data):
        user = Fournisseur.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nom=validated_data['nom'],
            tel=validated_data['tel']
        )
        return user

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'
        read_only_fields = ['montant_total', 'client', 'statut']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'