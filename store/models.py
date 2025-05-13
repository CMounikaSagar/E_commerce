from django.db import models
from category.models import *
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    Product_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=500,blank=True)
    Price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])
        
        
    def __str__(self):
        return self.Product_name
    