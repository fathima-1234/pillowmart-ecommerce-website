from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Account 
from .forms import Registrationform,AddressForm,UserForm
from django.contrib import messages, auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .otp import *
from django.core.paginator import Paginator
from requests.utils import urlparse
import random
import pyotp
from cart.models import  CartcartItem
from order.models import Order, OrderProduct,Address
# vertification email and reset password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


# Create your views here.


def register(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    form = Registrationform(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
           
      user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
      user.save()
      
      if user.is_active:
        messages.success(request, 'Phone verified')
        return redirect('login')
      else:
        totp = pyotp.TOTP(settings.OTP_SECRET)
        otp = totp.now()
        msg_html = render_to_string(
            'accounts/email.html', {'otp': otp})

        send_mail(f'Please verify your E-mail', f'Your One-Time Verification Password is {otp}', settings.EMAIL_HOST_USER, [
            email], html_message=msg_html, fail_silently=False)

        request.session['otp'] = otp
        request.session['email'] = email
        return redirect('verify_otp')
  else:    
    form = Registrationform()
  context = {
    'form': form
  }
  
  return render (request,'accounts/signup.html',context)  

def resend_otp(request, phone_number):
    email = request.POST['email']
      
  
    if User.objects.filter(email=email).exists():
        
        totp = pyotp.TOTP(settings.OTP_SECRET)
        otp = totp.now()
        msg_html = render_to_string(
            'accounts/email.html', {'otp': otp})

        send_mail(f'Please verify your E-mail', f'Your One-Time Verification Password is {otp}', settings.EMAIL_HOST_USER, [
            email], html_message=msg_html, fail_silently=False)

        request.session['otp'] = otp
        request.session['email'] = email
        return redirect('verify-otp') 

@never_cache
def verify_otp(request):
    if 'otp' not in request.session:
        return redirect('home')

    # if request.user.is_authenticated:
    #     return redirect('userDashboard')

    error = ''
    if request.method == 'POST':
        otp = request.session['otp']
        user_otp = request.POST['otp']

        if user_otp != '':
            email = request.session['email']

            if 'otp' in request.session and int(user_otp) == int(request.session['otp']):

                user = Account.objects.get(email=email)
                user.is_active = True
                user.save()
                del request.session['otp']
                del request.session['email']
                messages.success(
                    request, 'Phone verified, please login to continue')
                return redirect('login')
            else:
               return render(request, 'userapp/otpverification.html', {'error': 'Invalid OTP'})
    return render(request, 'accounts/otpverification.html', {'error':error})


@never_cache
def login(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(email=email, password=password)

    if user is not None:
      
      try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
        
        if is_cart_item_exists:
          cart_item = CartItem.objects.filter(cart=cart)
          
          product_variation = []
          for item in cart_item:
            variations = item.variations.all()
            product_variation.append(list(variations))
            
          cart_item = CartItem.objects.filter(user=user)
      
          ex_var_list = []
          id = []
          for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            
          for product in product_variation:
            if product in ex_var_list:
              index = ex_var_list.index(product)
              item_id = id[index]
              item = CartItem.objects.get(id=item_id)
              item.quantity += 1
              item.user = user
              item.save()
            else:
              cart_item = CartItem.objects.filter(cart=cart)    
              for item in cart_item:
                item.user = user
                item.save()
        
      except:
        pass
           
      auth.login(request, user)      # login without otp
      
    
    
  return render (request, 'accounts/signin.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')


# forgot passaword
def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if  Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)

            # reset email password
            current_site=get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('accounts/Reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request,'Account deos not exits')
            return redirect('forgot_password')
    return render(request,"accounts/forgot_password.html") 
   


def resetPassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    
def resetPassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if  password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset succesful')
            return redirect('login')
        
        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')


@login_required(login_url = 'login')
def userDashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id= request.user.id)
    orders_count = orders.count()
    context = {
        'orders_count':orders_count
    }
    return render(request, 'accounts/userDashboard.html')
  
@login_required(login_url='login')
def myOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders':page_obj
    }

    return render(request,'accounts/myOrders.html',context)

@login_required(login_url='login') 
def orderDetails(request,order_id):
    order_details = OrderProduct.objects.filter(order_id=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price * i.quantity
        
    context = {
        'order_details':order_details,
        'order':order,
        'subtotal':subtotal    
    }

    return render(request,'accounts/orderDetails.html',context)
  
@login_required(login_url='login') 
def editProfile(request):
  if request.method =='POST':
    form = UserForm(request.POST,instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request,'Your Profile Updated Successfully ')
      return redirect ('userDashboard')

  else:
      form = UserForm(instance=request.user)

  context = {
        'form':form
    } 

  return render(request,'accounts/editProfile.html', context)

@login_required(login_url='login') 
def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  
  context = {
    'address':address,
  }
  return render(request, 'accounts/myAddress.html', context)

@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.district =  form.cleaned_data['district']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.pincode =  form.cleaned_data['pincode']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('myAddress')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('myAddress')
    else:
        form = AddressForm()
        context={
            'form':form
        }    
    return render(request,'accounts/add-address.html',context)
  
@login_required(login_url='login')
def edit_address(request, id):
  address = Address.objects.get(id=id)
  if request.method == 'POST':
    form = AddressForm(request.POST, instance=address)
    if form.is_valid():
      form.save()
      messages.success(request , 'Address Updated Successfully')
      return redirect('myAddress')
    else:
      messages.error(request , 'Invalid Inputs!!!')
      return redirect('myAddress')
  else:
      form = AddressForm(instance=address)
      
  context = {
            'form' : form,
        }
  return render(request,'accounts/edit-address.html',context)

@login_required(login_url='login')
def delete_address(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('myAddress')

@login_required(login_url='login')
def changePassword(request):
    if request.method =='POST':
        currentPassword = request.POST['currentPassword']
        NewPassword = request.POST['NewPassword']
        confirmPassword = request.POST['confirmPassword']

        user = Account.objects.get(email__exact=request.user.email)
        
        if NewPassword == confirmPassword:
            success = user.check_password(currentPassword)
            if success:
                user.set_password(NewPassword)
                user.save()
                messages.success(request,'password updated succesfully')
                return redirect('changePassword')
            else:
                messages.error(request,'current password is wrong')
                return redirect('changePassword')
        else:
            messages.error(request,'password deos not match')
    
    return render(request,'accounts/changePassword.html')

