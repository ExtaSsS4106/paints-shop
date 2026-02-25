from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
from django.db import models
import json
import logging


# Авторизация / Регистрация
def index(request):
    return render(request, 'main/index.html')

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {"form": form})










# Функционал приложения

def catalog(request):
    products = Products.objects.all()
    
    pass

def about(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    pass



@login_required(login_url='/login')
def user_cart(request):
    usr_cart = Cart.objects.filter(user=request.user)
    
    pass

@login_required(login_url='/login')
def orders_list(request):
    usr_orders_list = Orders.objects.filter(user=request.user)
    
    pass

@login_required(login_url='/login')
def add_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        user = request.user
        bank_card = data.get('bank_card')
        cvc = data.get('cvc')
        card_data = data.get('card_data')
        address = data.get('address')
        
        if bank_card and cvc and card_data and address:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.bank_card = bank_card
            profile.cvc = cvc
            profile.card_data = card_data
            profile.address = address
            profile.save()
        else:
            pass
    pass

@login_required(login_url='/login')
def create_orders(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        orders = data.get('orders')
        user = request.user
        for order in orders:
            shipping_address = order.get('shipping_address')
            product = Products.objects.get(id=order.get('product'))
            quantity = order.get('quantity')
            if shipping_address and product and quantity:
                orders_table = Orders.objects.create(
                    user=user,
                    status = Orders.PROCESSING,
                    shipping_address = shipping_address,
                    product = product,
                    quantity = quantity
                )
    created_list_orders = Orders.objects.filter(user=request.user)


def search(request, query):
    data = Products.objects.filter(name__icontains=query)
    pass

@login_required(login_url='/login')
def cart_actions(request, query):
    if request.method == 'POST':
        user = request.user
        if query == 'delete':
            data = json.loads(request.body)
            item = data.get('item')
            product = Cart.objects.get(
                user = user,
                product__id=item.get('id')
            )
            product.delete()
        elif query == 'minus':
            data = json.loads(request.body)
            item = data.get('item')
            product = Cart.objects.get(
                user = user,
                product__id=item.get('id')
            )
            product.quantity = product.quantity - 1
            product.save()
        elif query == 'add':
            data = json.loads(request.body)
            item = data.get('item') 
            product, created = Cart.objects.update_or_create(
                user = user,
                product__id=item.get('id'),
                defaults={
                    'quantity': 1  
                }
            )
            if not created:
                product.quantity += 1
                product.save()
            
    pass

