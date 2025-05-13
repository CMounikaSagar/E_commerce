from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_name','Price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('Product_name',)}
admin.site.register(Product,ProductAdmin)