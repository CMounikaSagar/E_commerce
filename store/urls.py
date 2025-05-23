from django.urls import path
from .views import *

urlpatterns = [
    path("",store,name='store'),
    path("category/<slug:category_slug>/",store,name='products_by_category'),
    path("category/<slug:category_slug>/<slug:product_slug>/",product_detail,name='product_details'),
    path("search/",search,name='search')
]