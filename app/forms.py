from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True', 'class': 'form-control' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True', 'class': 'form-control' }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control' }))
    password1 = forms.CharField( label='Password',widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))
    password2 = forms.CharField( label='Confirm Password',widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))

class Meta:
    model = User
    fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField( label=' Old Password',widget=forms.PasswordInput(attrs={ 'autofocus':'True','autocomplete':'current-password','class':'form-control' }))
    new_password1 = forms.CharField( label='New Password',widget=forms.PasswordInput(attrs={ 'autofocus':'True','autocomplete':'current-password','class': 'form-control' }))
    new_password2 = forms.CharField( label='Confirm Password',widget=forms.PasswordInput(attrs={ 'autofocus':'True','autocomplete':'current-password','class': 'form-control' }))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1= forms.CharField( label=' New Password',widget=forms.PasswordInput(attrs={ 'autocomplete':'current-password','class':'form-control' }))
    new_password2= forms.CharField( label='  Confirm New Password',widget=forms.PasswordInput(attrs={ 'autocomplete':'current-password','class':'form-control' }))
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'stock', 'category', 'product_image']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=['name','locality','city','mobile','state','zipcode','mail']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),  # Fixed here
        }

#product review and rating         
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)])
        }
#product review and rating         