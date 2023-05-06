from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),

    path('verify_otp', views.verify_otp, name='verify_otp'),
    
    # path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('resetPassword_validate/<uidb64>/<token>/',views.resetPassword_validate,name='resetPassword_validate'),
    path('resetPassword/',views.resetPassword,name='resetPassword'),

    path('userDashboard/', views.userDashboard, name='userDashboard'),
    path('myOrders/', views.myOrders, name='myOrders'),
    path('orderDetails/<int:order_id>/', views.orderDetails, name='orderDetails'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('myAddress/', views.myAddress, name='myAddress'),
    path('add_address/', views.add_address, name='add_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('changePassword/',views.changePassword,name='changePassword'),
]