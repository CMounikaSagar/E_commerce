from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import *
from .forms import *
from .models import *
from store.models import *
import datetime
import json

# Create your views here.
def place_order(request,total = 0, quantity = 0, ):
    current_user = request.user
    
    # if the cart counter is less than or equal to zero redirect to store page
    
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    
    for cart_item_1 in cart_items:
        total += (cart_item_1.product.Price * cart_item_1.quantity)
        quantity += cart_item_1.quantity
    tax = (2 * total)/100
    grand_total = total+tax
    
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            # store all the billing info inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') # to get the user ip address
            data.save()
            
            # generate order number
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_Date = d.strftime("%Y%m%d")
            order_number = current_Date+str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user = current_user,is_ordered = False,order_number = order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'orders/payments.html',context)
        else:
            print(form.errors)
        return redirect('store')
    else:
        return redirect('checkout')
    
def place_order_1(request):
    
    # move the cartItems to orderproduct table
    
    cart_items = CartItem.objects.filter(user=request.user)
    # payment = Payment.objects.filter(user = request.user).last()
    
    for item in cart_items:
        # body = json.loads(request.body)
        order = Order.objects.filter(user = request.user,is_ordered = False).first()
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.Price
        # orderproduct.payment = payment
        orderproduct.order_number = order.order_number
        orderproduct.is_ordered = True
        orderproduct.save()
        
    # remove the quantity of sold items
    
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()
    
    #clear the cart
    
    CartItem.objects.filter(user=request.user).delete()
    
    return redirect('order_complete')

def order_complete(request):
    return render(request,'orders/order_complete.html')