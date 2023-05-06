
from django.db import models
from  Store.models import Product
from accounts.models import Account

# Create your models here.


class Cart(models.Model):
  cart_id = models.CharField(max_length=250, blank=True)
  date_added = models.DateField(auto_now_add=True)
  
  def __str__(self):
    return self.cart_id

class CartcartItem(models.Model):
    quantity=models.IntegerField(default=1)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    price = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    def total(self):
        return (self.quantity )*(self.product.offer_price())
    # def sub_total(self):
        # return int(self.price)*int(self.quantity)
    def __unicode__(self):
        return self.product

class Wishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)