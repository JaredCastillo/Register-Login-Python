import random
import string
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='Phone Number', max_length=15, required=True)

    class Meta: 
        model = User
        fields = ['first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            return forms.ValidationError('Las contraseñas no son iguales')
        return cd['password2']
    
    def generate_username(self):
         return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.generate_username()
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user