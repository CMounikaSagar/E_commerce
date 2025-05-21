from django.urls import path
from .views import *

urlpatterns = [
    path("",cart,name='cart'),
    path("add_cart/<int:product_id>/",add_cart,name='add_cart'),
    path("decrement/<int:product_id>/<int:cart_item_id>/",decreament,name='decrement'),
    path("remove_Cart/<int:product_id>/<int:cart_item_id>/",remove_Cart,name='remove_cart'),
    path('checckout/',checkout,name='checkout')
]