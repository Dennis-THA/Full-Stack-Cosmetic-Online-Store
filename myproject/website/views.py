from django. shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from .models import Member
from .forms import Memberform
from .forms import LoginForm
from django.contrib import messages
from .models import Item

def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if Member.objects.filter(email=email, password=password).exists():
                return redirect('home')  # Redirect to home upon successful login
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
  

def signup(request):
    if request.method == "POST":
        form = Memberform(request.POST or None)
        if form.is_valid():
            form.save()
            # # Hash the password
            # member.password = make_password(form.cleaned_data['password'])
            # member.save()
            return render(request, 'success.html', {})
        else:    
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            age = request.POST['age']
            phone = request.POST['phone']
            messages.success(request, ('Oops! Something went wrong. Please check the fields and try again.'))
            return render(request, 'signup.html', {'fname':fname,
                                                    'lname':lname,
                                                    'email':email,
                                                    'password':password,
                                                    'age':age,
                                                    'phone':phone,
                                                    })
    else:
        return render(request, 'signup.html', {})

def members(request) :
    all_members = Member.objects.all
    return render (request, 'members.html', {'all':all_members})

def success(request) :
    return render (request, 'success.html', {})

# def item_detail(request, item_id):
#     try:
#         item = get_object_or_404(Item, pk=item_id)
#         # Handle cases where fields might be missing
#         image = item.image if item.image else 'media/item_images/4.jpg'
#         context = {
#             'item': item,
#             'image': image,
#         }
#         return render(request, 'item_detail.html', context)
#     except Item.DoesNotExist:
#         # Handle the case where the item does not exist
#         return render(request, '404.html', status=404)