from django import forms
from Store.models import Product
from category.models import Category
from accounts.models import Account
from order.models import Coupon
import datetime




class DateInput(forms.DateInput):
    input_type = 'date'

# Create your models here.
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount','min_value','valid_at','active']
        widgets = {
                    'valid_at': DateInput(),
                    }
    def __init__(self, *args, **kwargs):
        super(CouponForm,self).__init__(*args, **kwargs)
        self.fields['valid_at'].widget.attrs['min'] = str(datetime.date.today())
        
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'