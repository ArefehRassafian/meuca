from django.shortcuts import render
from django.urls import reverse
import random

import random

from django.contrib.auth import login, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View

from products.models import Product
from .forms import RegisterForm, ProfileForm, ContactUsForm , CustomPasswordChangeForm , AddressForm
from .models import Message

User = get_user_model()


def login_(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        # username=request.POST.get("username")
        # password = request.POST.get("password")
        # user=authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     redirect(/)
        # return render(
        #     request,
        #     "sign_in_1.html"
        # )

        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            user = form.get_user()

            login(request, user)
            next_page = request.GET.get('next')
            if next_page:
                print ("hekjjj")
                return redirect(next_page)

            return redirect("accounts:profile")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "sign_in_1.html",
        {"form": form},
    )
# برای مدل به جای جلسه دو ویو پایین رو از کامنت در بیار و ویو های همنامش رو کامنت کن
# def forgot_password(request):
#     if request.user.is_authenticated:
#         return redirect("/")
#
#     if request.method == "POST":
#
#         phone_number = request.POST.get(
#             "phone_number",
#             ""
#         ).strip()
#
#         try:
#             user = User.objects.get(
#                 phone_number=phone_number
#             )
#
#         except User.DoesNotExist:
#
#             return render(
#                 request,
#                 "forgot_password.html",
#                 {
#                     "error": "این شماره تلفن ثبت‌نام نشده است."
#                 }
#             )
#
#         # حذف کدهای قبلی این کاربر
#         PasswordResetCode.objects.filter(
#             user=user
#         ).delete()
#
#         # ساخت کد 6 رقمی
#         code = str(
#             random.randint(100000, 999999)
#         )
#
#         # ذخیره کد
#         PasswordResetCode.objects.create(
#             user=user,
#             code=code,
#         )
#
#         # فعلاً به جای SMS در ترمینال چاپ می‌کنیم
#         print("=" * 40)
#         print("کد فراموشی رمز عبور")
#         print(f"شماره: {user.phone_number}")
#         print(f"کد: {code}")
#         print("=" * 40)
#
#         # ذخیره کاربر در session
#         request.session[
#             "password_reset_user_id"
#         ] = user.id
#
#         return redirect(
#             "accounts:verify_forgot_password"
#         )
#
#     return render(
#         request,
#         "forgot_password.html"
#     )
# def verify_forgot_password(request):
#
#     if request.user.is_authenticated:
#         return redirect("/")
#
#     user_id = request.session.get(
#         "password_reset_user_id"
#     )
#
#     if not user_id:
#         return redirect(
#             "accounts:forgot_password"
#         )
#
#     try:
#         user = User.objects.get(
#             id=user_id
#         )
#
#     except User.DoesNotExist:
#
#         request.session.pop(
#             "password_reset_user_id",
#             None
#         )
#
#         return redirect(
#             "accounts:forgot_password"
#         )
#
#     error = None
#
#     if request.method == "POST":
#
#         # گرفتن 6 رقم
#         code = "".join([
#             request.POST.get("code1", ""),
#             request.POST.get("code2", ""),
#             request.POST.get("code3", ""),
#             request.POST.get("code4", ""),
#             request.POST.get("code5", ""),
#             request.POST.get("code6", ""),
#         ])
#
#         try:
#
#             reset_code = PasswordResetCode.objects.get(
#                 user=user
#             )
#
#         except PasswordResetCode.DoesNotExist:
#
#             error = "کد تأیید وجود ندارد."
#
#         else:
#
#             if code == reset_code.code:
#
#                 # کد صحیح است
#                 reset_code.delete()
#
#                 # حذف session
#                 request.session.pop(
#                     "password_reset_user_id",
#                     None
#                 )
#
#                 # ورود کاربر
#                 login(
#                     request,
#                     user,
#                     backend="django.contrib.auth.backends.ModelBackend"
#                 )
#
#                 return redirect(
#                     "accounts:profile"
#                 )
#
#             else:
#
#                 error = "کد تأیید اشتباه است."
#
#     return render(
#         request,
#         "verify_forgot_password.html",
#         {
#             "error": error,
#             "phone_number": user.phone_number,
#         }
#     )




# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#
#     if request.method == "POST":
#         # username=request.POST.get("username")
#         # email = request.POST.get("email")
#         # ....
#         # errors
#         # User.objects.create_user(...)
#     #return render(
#     #request,
#     #"sign_in_1.html"
#    # )
#
#         form = RegisterForm(request.POST)
#
#         if form.is_valid():
#             form.is_manager = False
#
#
#             user = form.save()
#
#             messages.success(
#                 request,
#                 "ثبت ‌نام با موفقیت انجام شد."
#             )
#
#             return redirect("accounts:login")
#
#     else:
#         form = RegisterForm()
#
#     return render(
#         request,
#         "sign_up_1.html",
#         {"form": form},
#     )
def forgot_password(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        phone_number = request.POST.get(
            "phone_number",
            ""
        ).strip()

        try:
            user = User.objects.get(
                phone_number=phone_number
            )

        except User.DoesNotExist:

            return render(
                request,
                "forgot_password.html",
                {
                    "error": "این شماره تلفن ثبت‌نام نشده است."
                }
            )

        # ساخت کد 6 رقمی
        code = str(
            random.randint(100000, 999999)
        )

        # ذخیره اطلاعات در Session
        request.session["forgot_phone"] = phone_number
        request.session["forgot_code"] = code
        request.session["forgot_user_id"] = user.id
        request.session["forgot_attempts"] = 0
        request.session.set_expiry(120)

        # فعلاً به جای SMS
        # کد را در ترمینال چاپ می‌کنیم
        print("=" * 40)
        print("کد فراموشی رمز عبور")
        print(f"شماره تلفن: {phone_number}")
        print(f"کد: {code}")
        print("=" * 40)

        return redirect(
            "accounts:verify_forgot_password"
        )

    return render(
        request,
        "forgot_password.html"
    )


def verify_forgot_password(request):

    phone = request.session.get(
        "forgot_phone"
    )

    user_id = request.session.get(
        "forgot_user_id"
    )

    saved_code = request.session.get(
        "forgot_code"
    )

    attempts = request.session.get(
        "forgot_attempts",
        0
    )

    # Session وجود ندارد
    if not phone or not user_id or not saved_code:
        print("aduvAsdddddddddddddddddddddddddddd")

        return redirect(
            "accounts:forgot_password"

        )

    error = None

    if request.method == "POST":

        # حداکثر ۵ تلاش
        if attempts >= 5:

            request.session.flush()

            return redirect(
                "accounts:forgot_password"
            )

        code = "".join([
            request.POST.get("code1", ""),
            request.POST.get("code2", ""),
            request.POST.get("code3", ""),
            request.POST.get("code4", ""),
            request.POST.get("code5", ""),
            request.POST.get("code6", ""),
        ])

        # افزایش تلاش
        attempts += 1

        request.session["forgot_attempts"] = attempts

        # بررسی کد
        if code == saved_code:

            try:

                user = User.objects.get(
                    id=user_id,
                    phone_number=phone
                )

            except User.DoesNotExist:

                request.session.flush()

                return redirect(
                    "accounts:forgot_password"
                )

            # ورود کاربر
            login(
                request,
                user
            )

            # پاک کردن Session مربوط به فراموشی رمز
            request.session.pop(
                "forgot_phone",
                None
            )

            request.session.pop(
                "forgot_user_id",
                None
            )

            request.session.pop(
                "forgot_code",
                None
            )

            request.session.pop(
                "forgot_attempts",
                None
            )

            return redirect(
                "accounts:profile"
            )

        else:

            if attempts >= 5:

                request.session.flush()

                return redirect(
                    "accounts:forgot_password"
                )

            remaining = 5 - attempts

            error = (
                f"کد وارد شده اشتباه است. "
                f"{remaining} تلاش باقی مانده."
            )

    return render(
        request,
        "verify_forgot_password.html",
        {
            "error": error
        }
    )
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#
#     if request.method == "POST":
#
#         form = RegisterForm(request.POST)
#
#         if form.is_valid():
#             # User هنوز ساخته نمی‌شود
#             user = form.save(commit=False)
#
#             # اگر قبلاً یک ثبت‌نام نیمه‌کاره  وجود دارد
#             # آن را حذف می‌کنیم
#             PendingRegistration.objects.filter(
#                 phone_number=user.phone_number
#             ).delete()
#             PendingRegistration.objects.filter(
#                 username=user.username
#             ).delete()
#
#             # ساخت کد 6 رقمی
#             code = str(random.randint(100000, 999999))
#
#             # ذخیره موقت اطلاعات ثبت‌نام
#             pending = PendingRegistration.objects.create(
#                 username=user.username,
#                 first_name=user.first_name,
#                 last_name=user.last_name,
#                 phone_number=user.phone_number,
#                 password=user.password,
#                 code=code,
#             )
#
#             # ذخیره شناسه ثبت‌نام موقت در Session
#             request.session["pending_registration_id"] = pending.id
#
# #             # ارسال کد به ایمیل
# #             send_mail(
# #                 subject="کد تأیید ثبت‌نام",
# #                 message=f"""
# # سلام {user.first_name}
# #
# # کد تأیید ثبت‌نام شما:
# #
# # {code}
# #
# # این کد را در صفحه تأیید وارد کنید.
# # """,
# #                 from_email=None,
# #                 recipient_list=[user.email],
# #                 fail_silently=False,
# #             )
#             print(code)
#
#             return redirect("accounts:verify_email")
#
#     else:
#         form = RegisterForm()
#
#     return render(
#         request,
#         "sign_up_1.html",
#         {"form": form},
#     )
#
#
# def verify_email(request):
#     pending_id = request.session.get(
#         "pending_registration_id"
#     )
#
#     if not pending_id:
#         return redirect("accounts:signup")
#
#     try:
#         pending = PendingRegistration.objects.get(
#             id=pending_id
#         )
#     except PendingRegistration.DoesNotExist:
#         return redirect("accounts:signup")
#     error = None
#
#     if request.method == "POST":
#
#         code = "".join([
#             request.POST.get("code1", ""),
#             request.POST.get("code2", ""),
#             request.POST.get("code3", ""),
#             request.POST.get("code4", ""),
#             request.POST.get("code5", ""),
#             request.POST.get("code6", ""),
#         ])
#
#         if code == pending.code:
#
#             # ساخت User واقعی
#
#             user = User(
#                 username=pending.username,
#                 first_name=pending.first_name,
#                 last_name=pending.last_name,
#                 phone_number=pending.phone_number,
#             )
#
#             # پسورد از قبل hash شده است
#             user.password = pending.password
#
#             # کاربر فعال است چون ایمیل تأیید شده
#             user.is_active = True
#
#             user.save()
#
#             # حذف ثبت نام موقت
#             pending.delete()
#
#             # حذف session
#             request.session.pop(
#                 "pending_registration_id",
#                 None
#             )
#
#             return redirect("accounts:login")
#
#         else:
#
#             error = "کد تأیید اشتباه است."
#
#     return render(
#         request,
#         "verify_email.html", {"error": error}
#     )

def signup(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # بررسی شماره تلفن
            if User.objects.filter(
                phone_number=user.phone_number
            ).exists():

                form.add_error(
                    "phone_number",
                    "این شماره تلفن قبلاً ثبت نام کرده است."
                )

            # بررسی username
            elif User.objects.filter(
                username=user.username
            ).exists():

                form.add_error(
                    "username",
                    "این نام کاربری قبلاً استفاده شده است."
                )

            else:

                # ساخت کد ۶ رقمی
                code = str(
                    random.randint(100000, 999999)
                )

                # ذخیره اطلاعات ثبت نام در Session
                request.session["signup_username"] = user.username
                request.session["signup_first_name"] = user.first_name
                request.session["signup_last_name"] = user.last_name
                request.session["signup_phone"] = user.phone_number

                # پسورد قبلاً توسط UserCreationForm هش شده
                request.session["signup_password"] = user.password

                # ذخیره کد
                request.session["signup_code"] = code
                request.session["signup_attempts"] = 0
                request.session.set_expiry(120)

                # چاپ کد در Terminal
                print("=" * 40)
                print("کد تأیید ثبت نام")
                print(f"شماره تلفن: {user.phone_number}")
                print(f"کد: {code}")
                print("=" * 40)

                return redirect(
                    "accounts:verify_email"
                )

    else:

        form = RegisterForm()

    return render(
        request,
        "sign_up_1.html",
        {
            "form": form
        }
    )
def verify_email(request):

    # گرفتن اطلاعات ثبت نام از Session

    username = request.session.get(
        "signup_username"
    )

    first_name = request.session.get(
        "signup_first_name"
    )

    last_name = request.session.get(
        "signup_last_name"
    )

    phone_number = request.session.get(
        "signup_phone"
    )

    password = request.session.get(
        "signup_password"
    )

    saved_code = request.session.get(
        "signup_code"
    )
    attempts = request.session.get(
        "signup_attempts",
        0
    )

    # اگر Session وجود نداشت
    if not all([
        username,
        phone_number,
        password,
        saved_code
    ]):

        return redirect(
            "accounts:signup"
        )

    error = None

    if request.method == "POST":
        # حداکثر ۵ تلاش
        if attempts >= 5:
            request.session.flush()

            return redirect(
                "accounts:forgot_password"
            )

        code = "".join([
            request.POST.get("code1", ""),
            request.POST.get("code2", ""),
            request.POST.get("code3", ""),
            request.POST.get("code4", ""),
            request.POST.get("code5", ""),
            request.POST.get("code6", ""),
        ])
        attempts += 1

        request.session["signup_attempts"] = attempts

        if code == saved_code:

            # اطمینان دوباره از اینکه کاربر قبلاً ساخته نشده
            if User.objects.filter(
                username=username
            ).exists():

                error = "این نام کاربری قبلاً استفاده شده است."

            elif User.objects.filter(
                phone_number=phone_number
            ).exists():

                error = "این شماره تلفن قبلاً ثبت نام کرده است."

            else:

                # ساخت User واقعی
                user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    password=password,
                    is_active=True,
                )

                user.save()

                # پاک کردن اطلاعات ثبت نام از Session
                request.session.pop(
                    "signup_username",
                    None
                )

                request.session.pop(
                    "signup_first_name",
                    None
                )

                request.session.pop(
                    "signup_last_name",
                    None
                )

                request.session.pop(
                    "signup_phone",
                    None
                )

                request.session.pop(
                    "signup_password",
                    None
                )

                request.session.pop(
                    "signup_code",
                    None
                )
                request.session.pop(
                    "signup_attempts",
                    None
                )

                return redirect(
                    "accounts:login"
                )

        else:

            error = "کد تأیید اشتباه است."

    return render(
        request,
        "verify_email.html",
        {
            "error": error
        }
    )
@login_required
def signout(request):
    logout(request)
    # return redirect(reverse("accounts:without_entering" , args=[request.user.id], kwargs={"state":"ok"}))
    return redirect("products:without_entering")


# def without_entering(request):
# return render(request, "index.html")



@login_required
def contact_us(request):
    if request.method == "POST":
        # تاریخ امروز
        today = timezone.localdate()
        # تعداد پیام‌های این کاربر در امروز
        messages_count = Message.objects.filter(
            user=request.user,
            created_at=today
        ).count()
        form = ContactUsForm(request.POST, request.FILES)

        if form.is_valid():

            # اگر امروز 5 پیام فرستاده
            if messages_count >= 5:
                return redirect("accounts:nomessage")
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            Message.objects.create(
                user=request.user,
                title=title,
                text=text
            )
            return redirect("accounts:okmessage")
    else:
        form = ContactUsForm()

    return render(request, "contact_us.html", {'form': form})


# @login_required
# def okmessage(request):
#
#     return render(
#         request,
#         "okmessage.html",
#         {'state':"ok"}
#     )
@method_decorator(login_required, name='dispatch')
class OkMessage(TemplateView):
    template_name = "okmessage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["state"] = "ok"
        return context


# @login_required
# def nomessage(request):
#     return render(
#         request,
#         "okmessage.html",
#         {'state': "no"}
#     )
@method_decorator(login_required, name='dispatch')
class NoMessages(TemplateView):
    template_name = "okmessage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["state"] = "No"
        return context


# @login_required
# def profile(request):
#     if request.method == "POST":
#
#         form = ProfileForm(
#             request.POST,
#             request.FILES,
#             instance=request.user
#         )
#
#         if form.is_valid():
#             form.save()
#             return redirect("accounts:profile")
#
#     else:
#
#         form = ProfileForm(
#             instance=request.user
#         )
#
#     return render(
#         request,
#         "profile.html",
#         {
#             "form": form
#         }
#     )


@login_required
def profile(request):

    profile_form = ProfileForm(
        instance=request.user
    )

    password_form = CustomPasswordChangeForm(
        user=request.user
    )

    if request.method == "POST":

        if "update_profile" in request.POST:

            profile_form = ProfileForm(
                request.POST,
                request.FILES,
                instance=request.user
            )

            if profile_form.is_valid():
                user = profile_form.save()

                # # فقط فیلدهایی که کاربر واقعاً تغییر داده
                # for field in profile_form.changed_data:
                #     value = profile_form.cleaned_data.get(field)
                #
                #     # اگر مقدار خالی بود، مقدار قبلی را نگه دار
                #     if value not in [None, ""]:
                #         setattr(user, field, value)
                #
                # user.save()

                return redirect("accounts:profile")

        elif "change_password" in request.POST:

            password_form = CustomPasswordChangeForm(
                user=request.user,
                data=request.POST
            )

            if password_form.is_valid():
                user = password_form.save()

                update_session_auth_hash(
                    request,
                    user
                )

                return redirect("accounts:profile")

    return render(
        request,
        "profile.html",
        {
            "profile_form": profile_form,
            "password_form": password_form,
        }
    )
# def about_us(request):
#     return render(request,'about_us.html')
class AboutUs(TemplateView):
    template_name = "about_us.html"


class RulesAndQuestions(TemplateView):
    template_name = "rules_and_questions.html"



