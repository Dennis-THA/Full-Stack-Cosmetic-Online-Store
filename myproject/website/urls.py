from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.home, name="home"),
    path('product', views.product, name="product"),
    path('members', views.members, name="members"),
    path('login', views.login_user, name="login"),
    path('signup', views.signup, name="signup"),
    path('success', views.success, name="success"),
    path('product/<int:item_id>/', views.item_detail, name='product_detail'),
    # path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-quantity/<int:cart_item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('item/<int:item_id>/review/', views.add_review, name='add_review')
    # path('blog/create/', views.create_blog_post, name='create_blog_post'),
    # path('blog/<int:post_id>/', views.blog_post_detail, name='blog_post_detail'),
    # path('blog/', views.list_blog_posts, name='list_blog_posts'),
]
