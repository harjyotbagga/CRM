from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('user/', views.userPage, name='user'), 
    path('account/', views.accountSettings, name='account'),
    path('products/', views.products, name='products'),
    path('customer/<int:pk>/', views.customer, name='customer'),

    path('create_order/', views.create_order, name='create_order'),
    path('create_customer_order/<int:pk>/', views.create_customer_order, name='create_customer_order'),
    path('update_order/<int:pk>/', views.update_order, name='update_order'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    path('update_customer/<int:pk>/', views.update_customer, name='update_customer'),
    path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)