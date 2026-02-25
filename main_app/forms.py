from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

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