from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from Store .models import Product
from cart.models import CartcartItem
from order.models import OrderProduct
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from accounts.models import Account
from django.contrib import messages



# Create your views here.

def home(request):
    product=Product.objects.all().filter( is_available=True)
    context={
        'products':product,
       
    }
    return render(request,'home.html',context)
def blog(request):
    return render(request,'blog.html')