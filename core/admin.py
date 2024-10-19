from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Products)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Banner)
admin.site.register(Basket)
admin.site.register(BasketItem)