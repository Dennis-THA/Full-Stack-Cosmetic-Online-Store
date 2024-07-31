from django import forms
from .models import Member
from .models import Item

class Memberform(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['fname', 'lname', 'email', 'password', 'age', 'phone']
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'old_price', 'discount_label', 'image', 'image_hover']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        price = cleaned_data.get('price')
        old_price = cleaned_data.get('old_price')
        discount_label = cleaned_data.get('discount_label')
        image = cleaned_data.get('image')
        image_hover = cleaned_data.get('image_hover')

        if not title:
            raise forms.ValidationError('Title is required.')
        if not price:
            raise forms.ValidationError('Price is required.')
        if not old_price:
            raise forms.ValidationError('Old price is required.')
        if not discount_label:
            raise forms.ValidationError('Discount label is required.')
        if not image:
            raise forms.ValidationError('Image is required.')
        if not image_hover:
            raise forms.ValidationError('Image hover is required.')

        return cleaned_data