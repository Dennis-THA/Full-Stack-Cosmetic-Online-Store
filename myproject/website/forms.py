from django import forms
from .models import Member, Review
from django.forms import inlineformset_factory
from .models import Item, VariationImage



# class Memberform(forms.ModelForm):
#     class Meta:
#         model = Member
#         fields = ['fname', 'lname', 'email', 'password', 'age', 'phone']
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['fname', 'lname', 'email', 'password', 'age', 'phone', 'profile_pic']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def save(self, commit=True):
        member = super().save(commit=False)
        if commit:
            # Don't save the password here; handle it in the signup view
            # For instance, you can use a signal or handle it explicitly in the view
            member.save()
        return member
    
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
    
class VariationImageForm(forms.ModelForm):
    class Meta:
        model = VariationImage
        fields = ['image']

# Create a formset for VariationImage
VariationImageFormSet = inlineformset_factory(Item, VariationImage, form=VariationImageForm, extra=5)
    
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        }
    
# Blog and Reviews
# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['name', 'email', 'rating', 'title', 'content']
#         widgets = {
#             'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
#             'content': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(ReviewForm, self).__init__(*args, **kwargs)
        
#         if user and user.is_authenticated:
#             self.fields['name'].initial = f"{user.member.fname} {user.member.lname}"
#             self.fields['email'].initial = user.email
#             self.fields['name'].widget.attrs['readonly'] = True
#             self.fields['email'].widget.attrs['readonly'] = True
#         else:
#             self.fields['name'].widget.attrs.pop('readonly', None)
#             self.fields['email'].widget.attrs.pop('readonly', None)
# class BlogPostForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'content', 'image']
#         widgets = {
#             'content': forms.Textarea(attrs={'rows': 10}),
#         }
