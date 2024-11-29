from django import forms
from django.core.exceptions import ValidationError
from . models import User

class SignupForm(forms.Form):
    username=forms.CharField(max_length=150)
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
class LoginForm(forms.Form):
     username=forms.CharField(max_length=150)
     password=forms.CharField(widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
    password=forms.CharField(widget=forms.PasswordInput,required=False)

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken.")
        return email
    def save(self,commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
            if commit:
                 user.save()
        return user