from  django.urls import path
from.import views

#url patterns
urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payment',views.payment,name='payment'),
    path('orderCompleted/',views.orderCompleted,name='orderCompleted'),
    path("coupon/",views.coupon,name='coupon'),
    path("cash_on_delivery/<int:id>/",views.cash_on_delivery,name='cash_on_delivery'),
    path("cancel_order/<int:id>/",views.cancel_order,name='cancel_order'),
    path("return_order/<int:id>/",views.return_order,name='return_order'),
  
]