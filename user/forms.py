from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Review, Customer, ShippingAddress


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Ваш ник:",widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Ваш ник:", widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    email = forms.EmailField(label="Ваша почта:", widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password1 = forms.CharField(label="Придумайте пароль:", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'

        }
    ))
    password2 = forms.CharField(label="Подтвердите пароль:", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'

        }
    ))

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2'
        )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', )

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш отзыв ...'
            })
        }


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя ...'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша фамилия ...'
            })
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address', 'city', 'phone')
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес ...'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город ...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона ...'
            })
        }
