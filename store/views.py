from django.shortcuts import render,get_object_or_404
from .models import *
from category.models import *
from carts.models import *
from carts.views import _cart_id
from django.db.models import Q

# Create your views here.
def store(request,category_slug = None):
    categories = None
    Products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category = categories,is_available = True)
        product_count = Product.objects.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = Product.objects.count()
    context = {
        'products':products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product = single_product).exists()
    except Exception as e:
        raise e 
    context = {
        'single_product':single_product,
        'in_cart':in_cart
    }
    return render(request,'store/product-detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.order_by('-created_date').filter(Q(Product_name__icontains = keyword) | Q(slug__icontains = keyword))
            product_count = Product.objects.count()
            
    context = {
        'products':product,
        'product_count':product_count,
    }
            
    return render(request,'store/store.html',context)