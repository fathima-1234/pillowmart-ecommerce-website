
from django.shortcuts import render,get_object_or_404
from . models import Product
from category . models import Category
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from django.db.models import Q


# Create your views here.

def product_list(request,category_slug=None):
    categories=None
    products=None
    if  category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        paginator=Paginator(products,5)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    else:
        categories = Category.objects.all()
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
        if request.method == 'POST':
            min = request.POST['minamount']
            max = request.POST['maxamount']
            min_price = min
            max_price = max
            products = Product.objects.all().filter(Q(price__gte=min_price),Q(price__lte=max_price),is_available=True).order_by('price')
            product_count = products.count()
        paginator=Paginator(products,4)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    context={
            'products': paged_products,
            'product_count': product_count,
                }
    return render(request,'product_list.html',context)



def Single_product(request,category_slug,product_slug,):
    user = request.user
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context={
        'single_product': single_product,
        
    }
    return render(request,'single_product.html',context)

def search(request):
    if 'search' in request.GET:
         search=request.GET['search']
         if search:
             products=Product.objects.filter(Q(description__icontains=search) | Q(product_name__icontains=search))
             product_count = products.count()
    context={
        'products':products,
        'product_count':product_count,
    }

    return render(request,'product_list.html',context) 



