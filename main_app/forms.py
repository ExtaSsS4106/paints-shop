from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
import re

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    bank_card = forms.CharField(max_length=16,required=False)
    cvc = forms.CharField(max_length=3,required=False)
    card_data = forms.CharField(max_length=25, required=False)
    address = forms.CharField(required=False)
    
    class Meta:
        model = User  
        fields = ["username", 
                  "email", 
                  "password1", 
                  "password2"
                  ]  
    
    def clean_bank_card(self):
        bank_card = self.cleaned_data.get('bank_card')
        if bank_card:
            bank_card = bank_card.replace(' ', '')
            if not bank_card.isdigit():
                raise forms.ValidationError('Номер карты должен содержать только цифры')
            if len(bank_card) != 16:
                raise forms.ValidationError('Номер карты должен содержать 16 цифр')
        return bank_card
    
    def clean_cvc(self):
        cvc = self.cleaned_data.get('cvc')
        if cvc:
            cvc = cvc.replace(' ', '')
            if not cvc.isdigit():
                raise forms.ValidationError('CVC должен содержать только цифры')
            if len(cvc) != 3:
                raise forms.ValidationError('CVC должен содержать 3 цифры')
        return cvc
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()  
        
        if self.cleaned_data.get('bank_card') and self.cleaned_data.get('cvc') and self.cleaned_data.get('card_data') and self.cleaned_data.get('address'):
            UserProfile.objects.update_or_create(
                user=user,  
                defaults={  
                    'bank_card': self.cleaned_data.get('bank_card', ''),
                    'cvc': self.cleaned_data.get('cvc', ''),
                    'card_data': self.cleaned_data.get('card_data', ''),
                    'address': self.cleaned_data.get('address', '')
                }
            )
        
        return user
    
class UserProfileForm(forms.ModelForm):
    bank_card = forms.CharField(
        max_length=16,
        required=True,  
    )
    cvc = forms.CharField(
        max_length=4,
        required=True,  
    )
    card_data = forms.CharField(
        max_length=5,
        required=True,  
    )
    address = forms.CharField(
        required=True,  
    )
    
    class Meta:
        model = UserProfile
        fields = ['bank_card', 'cvc', 'card_data', 'address']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def clean_bank_card(self):
        """Валидация номера карты"""
        bank_card = self.cleaned_data.get('bank_card')
        if bank_card:
            bank_card = re.sub(r'[\s\-]', '', bank_card)
            
            if not bank_card.isdigit():
                raise forms.ValidationError('Номер карты должен содержать только цифры')
            
            if len(bank_card) not in [15, 16]:  
                raise forms.ValidationError('Номер карты должен содержать 15 или 16 цифр')
        
        return bank_card
    
    def clean_cvc(self):
        """Валидация CVC"""
        cvc = self.cleaned_data.get('cvc')
        if cvc:
            if not cvc.isdigit():
                raise forms.ValidationError('CVC должен содержать только цифры')
            
            if len(cvc) not in [3, 4]:
                raise forms.ValidationError('CVC должен содержать 3 или 4 цифры')
        
        return cvc
    
    def clean_card_data(self):
        """Валидация срока действия"""
        card_data = self.cleaned_data.get('card_data')
        if card_data:
            # Проверяем формат ММ/ГГ
            pattern = r'^(0[1-9]|1[0-2])\/([0-9]{2})$'
            if not re.match(pattern, card_data):
                raise forms.ValidationError('Неверный формат. Используйте ММ/ГГ (например, 12/25)')
        return card_data
    
    def save(self, commit=True):
        profile, created = UserProfile.objects.update_or_create(
            user=self.user,  
            defaults={
                'bank_card': self.cleaned_data.get('bank_card', ''),
                'cvc': self.cleaned_data.get('cvc', ''),
                'card_data': self.cleaned_data.get('card_data', ''),
                'address': self.cleaned_data.get('address', '')
            }
        )
        return profile
    
    