from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart)
]


