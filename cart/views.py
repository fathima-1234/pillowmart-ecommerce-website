from django.shortcuts import render,redirect
from Store.models import Product
from.models import CartcartItem,Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartcartItem,Cart
from order.models import Address, Coupon, UserCoupon
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.



def addtocart(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        user = request.user
        if CartcartItem.objects.filter(product=product,user=user).exists():
            return redirect('cart')
        else:
            CartcartItem.objects.create(product=product,user=user)
            return redirect('cart')
    else:
        messages.error(request,'login for making order')
        return redirect('login')
    

    
def RemoveFromCart(request,id):
    cartItem=CartcartItem.objects.get(id=id)
    cartItem.delete()
    return redirect('cart')


def CartQuantity(request,id,action):
    Quantity = CartcartItem.objects.get(id=id)
    if action=='increase':
        Quantity.quantity += 1
        Quantity.save()
    elif action=='decrease':
        Quantity.quantity -= 1
        Quantity.save()
    return redirect('cart')


def wishlist(request):
    user=request.user
    items=Wishlist.objects.filter(user=user)
    items_count=items.count()
    context={
        'items':items,
        'items_count':items_count,
    }
    
    return render(request,'wishlist.html',context)


def addToWishlist(request,id):
    if request.user.is_authenticated:
        user=request.user
        product=Product.objects.get(id=id)
        if Wishlist.objects.filter(product=product,user=user).exists():
            return redirect('wishlist')
        else:
            Wishlist.objects.create(product=product,user=user)
            return redirect('wishlist')
    else:
        messages.error(request,'login for making orders')
        return redirect('login')
    

def RemoveFromWishlist(request,id):
    wishlistItem=Wishlist.objects.get(id=id)
    wishlistItem.delete()
    return redirect('wishlist')     

 
@login_required(login_url = 'login')
def checkout2(request, total=0, quantity=0,items=None):
  tax=0
  
  total_price = 0
  address = Address.objects.filter(user = request.user)
  
  try:
    if request.user.is_authenticated:
      cart_items = CartcartItem.objects.filter(user = request.user, is_active=True)
    else:
      cart =Cart.objects.get(cart_id=_cart_id(request))
      cart_items = CartcartItem.objects.filter(cart=cart, is_active=True)

    for cart_item in cart_items:
      total_price += int(cart_item.product.offer_price())*int(cart_item.quantity)
      # total_price += cart_item.total()
      # total_price += int(cart_item.product.offer_price()) 
      quantity += cart_item.quantity
    tax = (5 * total_price)/100
    grand_total = total_price + tax
    grand_total = format(grand_total, '.2f')
  except ObjectDoesNotExist:
    pass
  
  coupons = Coupon.objects.filter(active = True)

  for item in coupons:
    try:
        coupon = UserCoupon.objects.get(user = request.user,coupon = item)
    except:
        coupon = UserCoupon()
        coupon.user = request.user
        coupon.coupon = item
        coupon.save() 


  coupons = UserCoupon.objects.filter(user = request.user, used=False)
  
  context = {
    'address':address,
    'total_price':total_price,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,
    'coupons':coupons,
  }
  return render(request, 'checkout2.html', context)




def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart


def cart(request, total=0, quantity=0, cart_items=None):
  tax=0
  grand_total = 0
  product_price = 0
  
  try:
    if request.user.is_authenticated:
      cart_items = CartcartItem.objects.filter(user = request.user, is_active=True).order_by('id')
      wishlist_items=Wishlist.objects.filter(user=request.user)
      wishlist_items_count=wishlist_items.count()
      
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_items = CartcartItem.objects.filter(cart=cart, is_active=True).order_by('id')
      
    for cart_item in cart_items:
      # price_mult = int(cart_item.variations.all().values_list('price_multiplier')[0][0])
      # product_price += int(cart_item.product.offer_price()) 
      # product_price += cart_item.total()
      product_price += int(cart_item.product.offer_price())*int(cart_item.quantity)
      quantity += cart_item.quantity
      # cart_item.price += product_price
      cart_item.save()
    tax = (5 * product_price)/100
    grand_total = product_price  + tax
    grand_total = format(grand_total, '.2f')
  except ObjectDoesNotExist:
    pass
  
  context = {
    'product_price':product_price,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,
    'item_count':'item_count'
  }
  return render(request, 'cart.html', context)