from django import forms
from .models import Member

class Memberform(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['fname', 'lname', 'email', 'password', 'age', 'phone']
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)