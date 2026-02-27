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
    return render(request, 'main/catalog.html', {'products':products})

def about(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    return render(request, 'main/about.html', {'product':product})



@login_required(login_url='/login')
def user_cart(request):
    usr_cart = Cart.objects.filter(user=request.user)
    return render(request, 'main/cart.html', {'usr_cart':usr_cart})

@login_required(login_url='/login')
def orders_list(request):
    usr_orders_list = Orders.objects.filter(user=request.user)
    return render(request, 'main/orders.html', {'usr_orders_list':usr_orders_list})


@login_required(login_url='/login')
def add_card(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
        
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/user_cart')
    else:
        form = UserProfileForm(
            instance=profile,
            user=request.user
        )
    return render(request, 'main/card.html', {'form':form})

@login_required(login_url='/login')
def create_orders(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('/add_card')
    else:
        user = request.user
        orders = Cart.objects.filter(user=user)
        for order in orders:
            shipping_address = profile.address
            product = order.product
            quantity = order.quantity
            if shipping_address and product and quantity:
                orders_table = Orders.objects.create(
                    user=user,
                    status = Orders.PROCESSING,
                    shipping_address = shipping_address,
                    product = product,
                    quantity = quantity
                )
                order.delete()
    return redirect('/orders_list')


def search(request):
    query = request.GET.get('q', '')
    if query == '':
        return redirect('/')
    products = Products.objects.filter(name__icontains=query)
    return render(request, 'main/catalog.html', {'products':products})

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
            return JsonResponse({'quantity': product.quantity})
        elif query == 'add':
            data = json.loads(request.body)
            item = data.get('item') 
            product, created = Cart.objects.get_or_create(
                user = user,
                product=Products.objects.get(id = item.get('id')),
                defaults={
                    'quantity': 1  
                }
            )
            if not created:
                product.quantity += 1
                print(product.quantity)
                product.save()
            return JsonResponse({'quantity': product.quantity})
    return JsonResponse({'quantity': product.quantity})
