from django. shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .models import Member
from .forms import LoginForm, MemberForm, ReviewForm
from django.http import JsonResponse
from django.db.models import Avg
from .forms import ItemForm, VariationImageFormSet
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Item, Cart, Review
from django.contrib.auth import update_session_auth_hash




def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def signup(request):
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)  # Include FILES for profile_pic
        if form.is_valid():
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']

            # Check if a user with this email already exists
            if User.objects.filter(username=email).exists():
                messages.error(request, 'A user with this email already exists.')
                return render(request, 'signup.html', {'form': form})

            # Create a User instance using create_user (handles password hashing)
            user = User.objects.create_user(username=email, email=email, password=raw_password)

            # Create and save the Member instance, linking to the User
            member = form.save(commit=False)
            member.user = user
            member.save()

            return redirect('success')
        else:
            messages.error(request, 'Error in the form. Please try again.')
    else:
        form = MemberForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home upon successful login
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def logout_user(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout



def members(request) :
    all_members = Member.objects.all
    return render (request, 'members.html', {'all':all_members})

def success(request) :
    return render (request, 'success.html', {})


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == 'POST':
        if 'review_form' in request.POST:  # Check if the form is a review form
            if request.user.is_authenticated:
                member = get_object_or_404(Member, user=request.user)
                name = f"{member.fname}"
                email = member.email
                profile_pic = member.profile_pic.url
            else:
                name = request.POST.get('name')
                email = request.POST.get('email')
                profile_pic = 'profile_pics/default-profile.webp'

            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.item = item
                review.name = name
                review.email = email
                review.profile_pic = profile_pic
                review.save()
                return redirect('product_detail', item_id=item.id)
        else:  # Existing functionality for item updates
            form = ItemForm(request.POST, request.FILES, instance=item)
            formset = VariationImageFormSet(request.POST, request.FILES, instance=item)
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                return redirect('product_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
        formset = VariationImageFormSet(instance=item)
        review_form = ReviewForm()

    reviews = Review.objects.filter(item=item)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    review_count = reviews.count()

    context = {
        'form': form,
        'formset': formset,
        'item': item,
        'review_form': review_form,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
    }

    if request.user.is_authenticated:
        member = get_object_or_404(Member, user=request.user)
        context['member'] = member

    return render(request, 'product_detail.html', context)



def cart(request):
    if request.user.is_authenticated:
        # For authenticated users
        cart_items = Cart.objects.filter(user=request.user)
    else:
        # For unauthenticated users
        cart_items = Cart.objects.filter(session_key=request.session.session_key)

    # Calculate total price and item count in the view
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    item_count = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'item_count': item_count,
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.user.is_authenticated:
        user = request.user
        session_key = None
    else:
        user = None
        session_key = request.session.session_key or request.session.create()
        request.session.save()

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        session_key=session_key,
        item=item,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')
def update_cart_quantity(request, cart_item_id):
    if request.method == "POST":
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

        # Get the cart item
        cart_item = get_object_or_404(Cart, id=cart_item_id)

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity = max(cart_item.quantity - 1, 1)  # Ensure quantity doesn't go below 1
        else:
            return HttpResponseBadRequest("Invalid action")

        cart_item.save()
        return redirect('cart')

    return HttpResponseBadRequest("Invalid request method")




def search(request):
    query = request.GET.get('q', '')
    items = Item.objects.filter(title__icontains=query)
    results = [{'id': item.id, 'title': item.title, 'image': item.image.url} for item in items]
    return JsonResponse({'items': results})

def product(request):
    items = Item.objects.all()
    return render(request, 'product.html', {'items': items})

@login_required
def profile_view(request):
    member = Member.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            # Save the form, but do not commit to the database yet
            member = form.save(commit=False)
            
            # If a new password is provided, update the user's password
            new_password = form.cleaned_data.get('password')
            if new_password:
                user = member.user
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after changing the password
            
            member.save()  # Save the Member instance
            return redirect('profile')  # Redirect to profile page after saving
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MemberForm(instance=member)
    
    return render(request, 'profile.html', {'form': form})

def add_review(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            member = get_object_or_404(Member, user=request.user)
            name = f"{member.fname} {member.lname}"
            email = member.email
            profile_pic = member.profile_pic
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            profile_pic = 'profile_pics/default-profile.webp'  # Path to default profile pic

        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.item = item
            review.name = name
            review.email = email
            review.profile_pic = profile_pic
            review.save()
            return redirect('product_detail', item_id=item.id)
        else:
            # Handle form errors
            return render(request, 'product_detail.html', {
                'item': item,
                'review_form': review_form,
                'error': 'Please correct the errors below.',
            })

    else:
        return redirect('product_detail', item_id=item.id)


