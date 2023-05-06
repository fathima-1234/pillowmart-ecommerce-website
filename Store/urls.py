from django.urls import path
from . import views


# urls of store
urlpatterns = [
    path('',views.product_list,name='product_list'),
    path('category/<slug:category_slug>/',views.product_list,name='products_by_category'),
    path('category<slug:category_slug>/<slug:product_slug>/',views.Single_product,name='Single_product'),
    path('search/',views.search,name='search'),
    # path('price_change/', views.price_change, name='price_change'),
    path('shop_filter/', views.product_list, name='shop_filter'),
    
]