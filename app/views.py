from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ClientRegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegisterSerializer
    
    @swagger_auto_schema(
        operation_description="Enregistrement d'un nouveau client",
        responses={201: ClientRegisterSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class FournisseurRegisterView(generics.CreateAPIView):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurRegisterSerializer
    
    @swagger_auto_schema(
        operation_description="Enregistrement d'un nouveau fournisseur",
        responses={201: FournisseurRegisterSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CategorieListCreateView(generics.ListCreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Liste toutes les catégories ou crée une nouvelle",
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Créer une nouvelle catégorie",
        security=[{'Bearer': []}]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProduitListCreateView(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    
    @swagger_auto_schema(
        operation_description="Liste tous les produits ou crée un nouveau",
        responses={200: ProduitSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Créer un nouveau produit",
        security=[{'Bearer': []}],
        responses={201: ProduitSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CommandeListCreateView(generics.ListCreateAPIView):
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, Client):
            return Commande.objects.filter(client=user)
        elif isinstance(user, Fournisseur):
            return Commande.objects.filter(produit__fournisseur=user)
        return Commande.objects.none()
    
    @swagger_auto_schema(
        operation_description="Liste toutes les commandes ou crée une nouvelle",
        security=[{'Bearer': []}],
        responses={200: CommandeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Créer une nouvelle commande",
        security=[{'Bearer': []}],
        responses={201: CommandeSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommandeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if isinstance(user, Client):
            return Commande.objects.filter(client=user)
        elif isinstance(user, Fournisseur):
            return Commande.objects.filter(produit__fournisseur=user)
        return Commande.objects.none()
    
    @swagger_auto_schema(
        operation_description="Récupère une commande spécifique",
        security=[{'Bearer': []}],
        responses={200: CommandeSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Met à jour une commande",
        security=[{'Bearer': []}],
        responses={200: CommandeSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Supprime une commande",
        security=[{'Bearer': []}],
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    @swagger_auto_schema(
        operation_description="Récupère le profil de l'utilisateur connecté",
        security=[{'Bearer': []}],
        responses={200: UtilisateurSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)