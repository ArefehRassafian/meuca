from accounts.models import User
from django import forms
from .models import Order



from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            "receiver_name",
            "receiver_phone",
            "email",
        ]

        widgets = {
            "receiver_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام گیرنده",
                }
            ),

            "receiver_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "09123456789",
                    "inputmode": "numeric",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@gmail.com",
                }
            ),
        }

# class OrderForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
#     address = forms.CharField(required=False)
#     status = forms.CharField(required=False)
#     is_paid = forms.BooleanField(required=False)
#     class Meta:
#         model = Order
#         fields ='__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for field in self.fields.values():
#             field.widget.attrs["class"] = "form-control"