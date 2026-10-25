

from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.password_validation import validate_password

from .models import User ,Address


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",

                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",

                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",

                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "inputmode": "numeric",
                }
            ),



            "password1": forms.PasswordInput(
                attrs={
                    "class": "form-control",

                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-control",

                }
            )

        }




class ProfileForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}), required=False)
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}) , required=False)
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "email",
            "picture",



        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",


                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",


                }
            ),

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",

                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",


                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",

                }
            ),

            "picture": forms.FileInput(
                attrs={
                    "accept": ".png, .jpg, .jpeg"
                }
            )

        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False
        self.fields["email"].required = False
        self.fields["picture"].required = False


    # def clean_password(self):
    #     password = self.cleaned_data.get("password")
    #     if password:
    #         validate_password(password, self.instance)
    #         return password
    #     return None
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     password2 = cleaned_data.get("password2")
    #     if password or password2:
    #         if password != password2:
    #             self.add_error("password2","رمز عبور ها با هم تطابق ندارند")
    #             return cleaned_data
    #     return cleaned_data
    #
    # def save(self, commit=True):
    #
    #     user = super().save(commit=False)
    #     password = self.cleaned_data.get("password")
    #     if password:
    #         user.set_password(password)
    #
    #     if commit:
    #         user.save()
    #     return user


class CustomPasswordChangeForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ContactUsForm(forms.Form):
    title= forms.CharField(widget=forms.TextInput(attrs={"class":"form-control",'placeholder':"..."}),max_length=50,label="عنوان",required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control",'placeholder':"..."}),label="متن" )


    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if 'a' in title:
    #         raise forms.ValidationError("error for %(title)s title2" , code="123" ,params={'title':title})
    #     return title
    # def clean(self):
    #     title=self.cleaned_data.get('title')
    #     text = self.cleaned_data.get('text')
    #     if 'a' in title:
    #         self.add_error('title',"error for title")
    #     if title == text:
    #         raise forms.ValidationError("error for title1")
    #
    #
    # in template : {{ form.non_field_errors }}





class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        fields = [
            "name",
            "province",
            "city",
            "address",
            "postal_code",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام گیرنده",
                }
            ),
            "province": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "استان",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شهر",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "آدرس کامل",
                    "rows": 3,
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "کد پستی",
                    "inputmode": "numeric",
                }
            ),
        }






#
# class AddressForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
#     class Meta:
#         model = Address
#         fields ='__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for field in self.fields.values():
#             field.widget.attrs["class"] = "form-control"