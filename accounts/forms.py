from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
User = get_user_model()
from .models import Profile, ShippingAddress , BillingAddress

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=("E-mail"), max_length=75)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="",
                               max_length=32, help_text="<small id='emailHelp' class='form-text text-muted'>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(label="",
                                 max_length=32, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="",
                                max_length=32, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label="",
                             max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label="", help_text="<small><ul class='form-text text-muted'><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul></small>",
                                max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label="", help_text="<small class='form-text text-muted'>Enter the same password as before, for verification.</small>",
                                max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    phone = forms.CharField(label="",
                                 max_length=32, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))
    address = forms.CharField(label="",
                                 max_length=32, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    class Meta:
        model = get_user_model()
        fields = ('email', 'username','first_name','last_name','phone','address')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ''


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('name', 'phone', 'address',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'address',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name',)

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('full_name', 'phone','city','area', 'address','address_type')

class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('full_name', 'phone','city','area', 'address','address_type')