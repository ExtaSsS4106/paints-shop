
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.index, name='index'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('logout', views.logout_view, name='logout'),
    
    path('', views.catalog, name='catalog'),
    
    path('about/product/<int:product_id>/', views.about, name='about'),
    
    path('user_cart', views.user_cart, name='user_cart'),
    path('orders_list', views.orders_list, name='orders_list'),
    path('add_card', views.add_card, name='add_card'),
    path('create_orders', views.create_orders, name='create_orders'),
    
    path('search/', views.search, name='search'),
    path('cart_actions/<str:query>/', views.cart_actions, name='cart_actions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
