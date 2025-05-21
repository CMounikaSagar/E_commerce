from django.db import models
from accounts.models import *
from store.models import *

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    Payment_id = models.CharField(max_length=200,null=True,blank=True,default=None)
    payment_method = models.CharField(max_length=200)
    amount_paid = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Payment_id
    
class Order(models.Model):
    status = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    # Payment = models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    order_number = models.CharField(max_length=20,unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    order_note = models.CharField(max_length=100,blank=True)
    order_total = models.FloatField()
    tax = models.CharField(max_length=100,choices=status,default='New')
    status = models.CharField(blank=True,max_length=10)
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.Product_name