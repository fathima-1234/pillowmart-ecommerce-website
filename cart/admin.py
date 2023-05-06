from django.contrib import admin
from . models import CartcartItem,Wishlist,Cart


class CartAdmin(admin.ModelAdmin):
  list_display = ('cart_id', 'date_added',)

  
class CartcartItemAdmin(admin.ModelAdmin):
  list_display = ('product', 'cart', 'quantity', 'is_active')

# Register your models here.
admin.site.register(CartcartItem,CartcartItemAdmin)
admin.site.register(Wishlist)

admin.site.register(Cart, CartAdmin)
