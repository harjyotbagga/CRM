from django import forms
from django.forms import ModelForm
from .models import Tag, Customer, Order, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Enter your name.', widget=forms.TextInput(attrs={'placeholder':'first_name'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder':'last_name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}), max_length=254, help_text='Enter a valid email address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

