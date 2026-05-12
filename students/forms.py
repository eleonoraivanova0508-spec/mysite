from django import forms
from .models import Grade
from .models import Profile
from django.contrib.auth.models import User

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score', 'homework_comment']
        
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data



class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}))
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'phone']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о себе...'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67'}),
        }
        labels = {
            'avatar': 'Аватар',
            'bio': 'О себе',
            'phone': 'Телефон',
        }