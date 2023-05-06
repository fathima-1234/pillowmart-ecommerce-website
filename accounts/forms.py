from django import forms
from . models import Account
from order.models import Address
from django.contrib import messages

class Registrationform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password']
    

    #  for checking the password and confirm password are equal
    def clean(self):
        cleaned_data=super(Registrationform,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password !=confirm_password:
            raise forms.ValidationError("entered passwords deos not match each other!")


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields  = ['first_name','last_name', 'email', 'phone_number',]

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)  
        for field  in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'
             
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line1','address_line2','district','state','city', 'pincode']
    
    def __init__(self, *args, **kwargs):
      super(AddressForm,self).__init__(*args, **kwargs)  
      for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'