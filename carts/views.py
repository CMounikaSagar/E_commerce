from django.shortcuts import render,redirect,get_object_or_404
from store.models import *
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

#create and get session id for cart

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# add cart item and assign to the user
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create cart by session
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    if request.user.is_authenticated:
        # Check if the cart item already exists for the authenticated user
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={'cart': cart, 'quantity': 1}
        )
    else:
        # For unauthenticated users, use the session cart
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            user=None,
            defaults={'quantity': 1}
        )

    if not created:
        # If already exists, just increment the quantity
        cart_item.quantity += 1
    else:
        # If newly created and user is authenticated, assign the cart
        if request.user.is_authenticated:
            cart_item.cart = cart

    cart_item.save()
    return redirect('cart')  # or your cart page route name
        
def decreament(request,product_id,cart_item_id=None):
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.get(product = product,user = request.user,id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.get(product = product,cart = cart,id=cart_item_id)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()
    except:
        pass
    
    return redirect('cart')

def remove_Cart(request, product_id, cart_item_id=None):
    print(f'entered into remove view{product_id},{cart_item_id}')
    product = get_object_or_404(Product, id=product_id)
    print(product)
    try:
        print("entered into try block")
        if request.user.is_authenticated:
            print('user authenticated')
            # Get the cart item for the authenticated user
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            print(cart_item)
        else:
            # Get the cart using the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        # Remove the cart item
        cart_item.delete()

    except CartItem.DoesNotExist:
        print("CartItem not found. Nothing to delete.")

    return redirect('cart')
    

def cart(request,total = 0, quantity = 0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user,is_active = True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart,is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.Price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total+tax
    except Exception as e:
        pass
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'store/cart.html',context)

@login_required(login_url='login')
def checkout(request,total = 0, quantity = 0, cart_items = None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart,is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.Price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total+tax
    except Exception as e:
        pass
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'store/checkout.html',context)