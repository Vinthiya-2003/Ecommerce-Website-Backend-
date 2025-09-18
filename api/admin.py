from django.contrib import admin
from .models import Product, CartItem,Category

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Category)
