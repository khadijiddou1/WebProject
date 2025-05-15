from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


urlpatterns = [
    # Authentication
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registration
    path('api/register/client/', ClientRegisterView.as_view(), name='register_client'),
    path('api/register/fournisseur/', FournisseurRegisterView.as_view(), name='register_fournisseur'),
    
    # User
    path('api/user/profile/', UserProfileView.as_view(), name='user_profile'),
    
    # Categories
    path('api/categories/', CategorieListCreateView.as_view(), name='category_list_create'),
    
    # Products
    path('api/products/', ProduitListCreateView.as_view(), name='product_list_create'),
    
    # Orders
    path('api/orders/', CommandeListCreateView.as_view(), name='order_list_create'),
    path('api/orders/<int:pk>/', CommandeDetailView.as_view(), name='order_detail'),
    
   
]