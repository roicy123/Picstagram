from django.contrib import admin

from marketplace.models import Product,CartItem,Order,Payment

# Register your models here.
admin.site.register(Product),
admin.site.register(CartItem),

admin.site.register(Order),
admin.site.register(Payment),