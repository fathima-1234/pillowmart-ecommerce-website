from django.contrib import admin
from.models import Order,OrderProduct,Payment,Address,Coupon,UserCoupon




class OrderProductInline(admin.TabularInline):
  model = OrderProduct
  extra = 0

class OrderAdmin(admin.ModelAdmin):
  list_display = ['order_number', 'phone', 'email', 'order_total', 'status','is_orderd']
  list_per_page =  20
  inlines = [OrderProductInline]
# Register your models here.
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,)
admin.site.register(Payment)
admin.site.register(Address,)
admin.site.register(Coupon)
admin.site.register(UserCoupon)