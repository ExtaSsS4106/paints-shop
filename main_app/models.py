from django.db import models
from django.contrib.auth.models import User
import secured_fields

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bank_card = secured_fields.EncryptedCharField(max_length=16, blank=True, null=True)
    cvc = secured_fields.EncryptedCharField(max_length=4, blank=True, null=True)
    card_data = secured_fields.EncryptedCharField(max_length=25, blank=True, null=True)
    address = secured_fields.EncryptedTextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username