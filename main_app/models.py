from django.db import models
from django.contrib.auth.models import User
import secured_fields
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bank_card = secured_fields.EncryptedCharField(max_length=16, blank=True, null=True)
    cvc = secured_fields.EncryptedCharField(max_length=4, blank=True, null=True)
    card_data = secured_fields.EncryptedCharField(max_length=25, blank=True, null=True)
    address = secured_fields.EncryptedTextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    
class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    img = models.CharField(max_length=255)
    count_in_storage = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    
    def __str__(self):
        return self.id, self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.id, self.user.username

class Orders(models.Model):
    
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [(PENDING, 'Pending'), (PROCESSING, 'Processing'), (COMPLETED, 'Completed'), (CANCELLED, 'Cancelled')]
    id = models.AutoField(primary_key=True)
    
    order_number = models.UUIDField(
        default=uuid.uuid4,  # Генерируется автоматически
        editable=False,      # Нельзя изменить
        unique=True,         # Уникальное значение
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING,verbose_name='Статус заказа')
    total_amount = models.IntegerField()
    shipping_address = models.CharField(max_length=255)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        if self.product and self.quantity:
            self.total_amount = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.order_number) 
    
    
    