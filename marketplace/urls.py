from django.urls import path
from . import views
from  authy.views import UserProfile

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    # Ensure payment-success is before <username>/
    path('payment-success/', views.payment_success, name='payment_success'),

    # User profile should be last
    path('<username>/', UserProfile, name='profile'),

]
