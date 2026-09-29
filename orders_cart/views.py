from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from accounts.models import Address
from orders_cart.cart_madule import Cart
from products.models import Product
from accounts.forms import AddressForm
from .forms import OrderForm
from .models import Order, OrderItem


class CartDetails(View):
    def get(self, request):
        cart = Cart(request)
        s = 0
        sd = 0
        for item in cart:
            s += (int(item["price"]) * int(item["quantity"]))
            sd += Product.objects.filter(pk=int(item["id"])).first().final_price * int(item["quantity"])
        d = s - sd
        m = (sd * 10) / 100
        sdms = m + sd + 50000

        return render(request, "cart.html", {"cart": cart, "d": d, "s": s, "sdms": sdms, "m": m})


class HeaderCart(View):
    def get(self, request):
        cart = Cart(request)
        sd = 0
        quantity = 0
        for item in cart:
            sd = (sd + Product.objects.filter(pk=int(item["id"])).first().final_price) * int(item["quantity"])
            quantity += item["quantity"]

        return render(request, "partials/header.html", {"cart": cart, "sd": sd, "quantity": quantity})


class CartAdd(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.add(product)
        return redirect(request.META.get('HTTP_REFERER', '/'))


class CartSub(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.sub(product)
        return redirect('orders_cart:cart_details')


class CartDelete(View):
    def get(self, request, pk):
        cart = Cart(request)
        cart.delete(pk)
        return redirect(request.META.get('HTTP_REFERER', '/'))


@method_decorator(login_required, name="dispatch")
class Checkout(View):
    template_name = "checkout.html"

    # =====================================================
    # ابزارهای کمکی
    # =====================================================

    def get_addresses(self, request):
        """
        فقط آدرس‌های متعلق به کاربر لاگین شده
        """

        return Address.objects.filter(
            user=request.user
        ).order_by("-id")

    def get_cart(self, request):
        """
        دریافت سبد خرید فعلی کاربر
        """

        return Cart(request)

    def get_checkout_order(self, request):
        """
        بررسی می‌کند آیا این کاربر یک سفارش
        پرداخت‌نشده و در انتظار پرداخت دارد یا خیر.
        """

        order_id = request.session.get(
            "checkout_order_id"
        )

        # -------------------------------------------------
        # اگر Session دارای Order ID باشد
        # -------------------------------------------------

        if order_id:

            order = Order.objects.filter(
                id=order_id,
                user=request.user,
                status="waiting_payment",
                is_paid=False,
            ).first()

            if order:
                return order

            request.session.pop(
                "checkout_order_id",
                None
            )

        # -------------------------------------------------
        # پیدا کردن آخرین سفارش پرداخت‌نشده
        # -------------------------------------------------

        order = Order.objects.filter(
            user=request.user,
            status="waiting_payment",
            is_paid=False,
        ).order_by("-id").first()

        if order:
            request.session[
                "checkout_order_id"
            ] = order.id

            request.session.modified = True

        return order

    # =====================================================
    # قیمت کل Cart با احتساب تخفیف
    # =====================================================

    def get_cart_total_with_discount(self, cart):
        """
        قیمت کل محصولات سبد خرید
        با احتساب تخفیف هر محصول
        """

        total = 0

        for item in cart:

            price = int(
                item.get("price") or 0
            )

            quantity = int(
                item.get("quantity") or 0
            )

            product_id = item.get("id")

            product = Product.objects.filter(
                pk=product_id
            ).first()

            if product is None:
                continue

            final_price = int(
                product.final_price or 0
            )

            total += final_price * quantity

        return total

    # =====================================================
    # قیمت نهایی با مالیات و ارسال
    # =====================================================

    def get_final_price(self, cart):
        """
        قیمت نهایی:

        قیمت محصولات با تخفیف
        +
        10 درصد مالیات
        +
        50000 هزینه ارسال
        """

        cart_total = self.get_cart_total_with_discount(
            cart
        )

        tax = cart_total * 10 / 100

        shipping_cost = 50000

        final_price = (
                cart_total
                + tax
                + shipping_cost
        )

        return final_price

    # =====================================================
    # ساخت متن Snapshot آدرس
    # =====================================================
    def make_address_snapshot(self, address):
        """
        اطلاعات Address را به صورت متن داخل Order ذخیره می‌کند.
        """

        return (
            f"{address.province}، "
            f"{address.city}، "
            f"{address.address}، "
            f"کدپستی: "
            f"{address.postal_code}"
        )

    # =====================================================
    # ساخت OrderItemها از روی Cart
    # =====================================================

    def sync_order_items(self, order, cart):
        """
        OrderItemهای Order را دقیقاً مطابق Cart فعلی می‌کند.
        """

        # -------------------------------------------------
        # حذف آیتم‌های قبلی
        # -------------------------------------------------

        order.items.all().delete()

        # -------------------------------------------------
        # ساخت آیتم‌های جدید
        # -------------------------------------------------

        for item in cart:

            # ---------------------------------------------
            # Product ID
            # ---------------------------------------------

            try:

                product_id = int(
                    item["id"]
                )

            except (
                    KeyError,
                    TypeError,
                    ValueError
            ):

                raise ValueError(
                    "اطلاعات یکی از محصولات "
                    "سبد خرید معتبر نیست."
                )

            # ---------------------------------------------
            # پیدا کردن محصول
            # ---------------------------------------------

            product = Product.objects.filter(
                pk=product_id
            ).first()

            if product is None:
                raise ValueError(
                    "یکی از محصولات سبد خرید "
                    "دیگر وجود ندارد."
                )

            # ---------------------------------------------
            # Quantity
            # ---------------------------------------------

            try:

                quantity = int(
                    item["quantity"]
                )

            except (
                    KeyError,
                    TypeError,
                    ValueError
            ):

                raise ValueError(
                    "تعداد یکی از محصولات "
                    "معتبر نیست."
                )

            if quantity <= 0:
                raise ValueError(
                    "تعداد یکی از محصولات "
                    "معتبر نیست."
                )

            # ---------------------------------------------
            # Price
            # ---------------------------------------------

            try:

                price = int(
                    item["price"]
                )

            except (
                    KeyError,
                    TypeError,
                    ValueError
            ):

                raise ValueError(
                    "قیمت یکی از محصولات "
                    "معتبر نیست."
                )

            if price < 0:
                raise ValueError(
                    "قیمت یکی از محصولات "
                    "معتبر نیست."
                )

            # ---------------------------------------------
            # قیمت نهایی فعلی Product
            # ---------------------------------------------

            final_price = int(
                product.final_price or 0
            )

            # ---------------------------------------------
            # محاسبه درصد تخفیف
            # ---------------------------------------------

            if (
                    price > 0
                    and final_price < price
            ):

                discount_percent = round(
                    (
                            (
                                    price
                                    - final_price
                            )
                            / price
                    ) * 100
                )

            else:

                discount_percent = 0
            # ---------------------------------------------
            # محدود کردن تخفیف
            # ---------------------------------------------

            discount_percent = max(
                0,
                min(
                    100,
                    discount_percent
                )
            )

            # ---------------------------------------------
            # ساخت OrderItem
            # ---------------------------------------------

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                discount_percent=discount_percent,
            )

    # =====================================================
    # GET
    # =====================================================

    def get(self, request):

        # -------------------------------------------------
        # آدرس‌ها
        # -------------------------------------------------

        addresses = self.get_addresses(
            request
        )

        # -------------------------------------------------
        # Cart فعلی
        # -------------------------------------------------

        cart = self.get_cart(
            request
        )

        # -------------------------------------------------
        # محاسبه قیمت‌ها
        # -------------------------------------------------

        cart_total_with_discount = (
            self.get_cart_total_with_discount(
                cart
            )
        )

        final_price = self.get_final_price(
            cart
        )

        # -------------------------------------------------
        # Order پرداخت‌نشده قبلی
        # -------------------------------------------------

        order = self.get_checkout_order(
            request
        )

        # -------------------------------------------------
        # فرم آدرس
        # -------------------------------------------------

        form1 = AddressForm()

        # -------------------------------------------------
        # فرم سفارش
        # -------------------------------------------------

        if order:

            form2 = OrderForm(
                instance=order
            )

        else:

            form2 = OrderForm()

        return render(
            request,
            self.template_name,
            {
                "form1": form1,
                "form2": form2,
                "addresses": addresses,
                "order": order,
                "cart": cart,

                # قیمت‌ها
                "cart_total_with_discount": (
                    cart_total_with_discount
                ),
                "final_price": final_price,
            }
        )

    # =====================================================
    # POST
    # =====================================================

    def post(self, request):

        # =================================================
        # Cart فعلی
        # =================================================

        cart = self.get_cart(
            request
        )

        # =================================================
        # قیمت‌های Checkout
        # =================================================

        cart_total_with_discount = (
            self.get_cart_total_with_discount(
                cart
            )
        )

        final_price = self.get_final_price(
            cart
        )

        # =================================================
        # افزودن آدرس
        # =================================================

        if "address" in request.POST:

            form1 = AddressForm(
                request.POST
            )

            addresses = self.get_addresses(
                request
            )

            # ---------------------------------------------
            # حداکثر 3 آدرس
            # ---------------------------------------------

            if addresses.count() >= 3:
                order = self.get_checkout_order(
                    request
                )

                return render(
                    request,
                    self.template_name,
                    {
                        "form1": form1,
                        "form2": (
                            OrderForm(
                                instance=order
                            )
                            if order
                            else OrderForm()
                        ),
                        "addresses": addresses,
                        "order": order,
                        "cart": cart,
                        "cart_total_with_discount": (
                            cart_total_with_discount
                        ),
                        "final_price": final_price,
                        "error": (
                            "شما حداکثر می‌توانید "
                            "۳ آدرس ذخیره کنید."
                        ),
                    }
                )

            # ---------------------------------------------
            # اعتبارسنجی
            # ---------------------------------------------

            if form1.is_valid():
                address = form1.save(
                    commit=False
                )

                address.user = request.user

                address.save()

                order = self.get_checkout_order(
                    request
                )

                return render(
                    request,
                    self.template_name,
                    {
                        "form1": AddressForm(),

                        "form2": (
                            OrderForm(
                                instance=order
                            )
                            if order
                            else OrderForm()
                        ),

                        "addresses": self.get_addresses(
                            request
                        ),

                        "order": order,

                        "cart": cart,

                        "cart_total_with_discount": (
                            cart_total_with_discount
                        ),

                        "final_price": final_price,

                        "success": (
                            "آدرس با موفقیت "
                            "اضافه شد."
                        ),
                    }
                )

            # ---------------------------------------------
            # فرم نامعتبر
            # ---------------------------------------------

            order = self.get_checkout_order(
                request
            )

            return render(
                request,
                self.template_name,
                {
                    "form1": form1,

                    "form2": (
                        OrderForm(
                            instance=order
                        )
                        if order
                        else OrderForm()
                    ),

                    "addresses": addresses,

                    "order": order,

                    "cart": cart,

                    "cart_total_with_discount": (
                        cart_total_with_discount
                    ),

                    "final_price": final_price,
                }
            )

        # =================================================
        # ثبت سفارش و رفتن به پرداخت
        # =================================================

        if "payment" in request.POST:

            # -------------------------------------------------
            # اگر Cart خالی است
            # -------------------------------------------------

            if len(cart) == 0:
                return redirect(
                    "orders_cart:cart_details"
                )

            # =================================================
            # آدرس‌ها
            # =================================================
            addresses = self.get_addresses(
                request
            )

            address_id = request.POST.get(
                "address_id"
            )

            # -------------------------------------------------
            # آدرس انتخاب نشده
            # -------------------------------------------------

            if not address_id:
                return render(
                    request,
                    self.template_name,
                    {
                        "form1": AddressForm(),

                        "form2": OrderForm(
                            request.POST
                        ),

                        "addresses": addresses,

                        "order": self.get_checkout_order(
                            request
                        ),

                        "cart": cart,

                        "cart_total_with_discount": (
                            cart_total_with_discount
                        ),

                        "final_price": final_price,

                        "error": (
                            "لطفاً یک آدرس "
                            "انتخاب کنید."
                        ),
                    }
                )

            # -------------------------------------------------
            # بررسی مالکیت Address
            # -------------------------------------------------

            address = addresses.filter(
                id=address_id
            ).first()

            if address is None:
                return render(
                    request,
                    self.template_name,
                    {
                        "form1": AddressForm(),

                        "form2": OrderForm(
                            request.POST
                        ),

                        "addresses": addresses,

                        "order": self.get_checkout_order(
                            request
                        ),

                        "cart": cart,

                        "cart_total_with_discount": (
                            cart_total_with_discount
                        ),

                        "final_price": final_price,

                        "error": (
                            "آدرس انتخاب شده "
                            "معتبر نیست."
                        ),
                    }
                )

            # =================================================
            # Order قبلی
            # =================================================

            order = self.get_checkout_order(
                request
            )

            # =================================================
            # OrderForm
            # =================================================

            if order:

                form2 = OrderForm(
                    request.POST,
                    instance=order
                )

            else:

                form2 = OrderForm(
                    request.POST
                )

            # -------------------------------------------------
            # اعتبارسنجی فرم
            # -------------------------------------------------

            if not form2.is_valid():
                return render(
                    request,
                    self.template_name,
                    {
                        "form1": AddressForm(),

                        "form2": form2,

                        "addresses": addresses,

                        "order": order,

                        "cart": cart,

                        "cart_total_with_discount": (
                            cart_total_with_discount
                        ),

                        "final_price": final_price,
                    }
                )

            # =================================================
            # Transaction
            # =================================================

            try:

                with transaction.atomic():
                    # =========================================
                    # اگر Order وجود ندارد
                    # =========================================

                    if order is None:

                        order = form2.save(
                            commit=False
                        )

                        order.user = request.user

                        order.status = (
                            "waiting_payment"
                        )

                        order.is_paid = False


                    # =========================================
                    # اگر Order وجود داشته
                    # =========================================

                    else:

                        order.receiver_name = (
                            form2.cleaned_data[
                                "receiver_name"
                            ]
                        )

                        order.receiver_phone = (
                            form2.cleaned_data[
                                "receiver_phone"
                            ]
                        )

                        order.email = (
                            form2.cleaned_data.get(
                                "email"
                            )
                        )

                        order.status = (
                            "waiting_payment"
                        )

                        order.is_paid = False

                    # =================================================
                    # اطلاعات گیرنده
                    # =================================================

                    order.receiver_name = (
                        form2.cleaned_data[
                            "receiver_name"
                        ]
                    )

                    order.receiver_phone = (
                        form2.cleaned_data[
                            "receiver_phone"
                        ]
                    )

                    # =================================================
                    # Email
                    # =================================================

                    email = form2.cleaned_data.get(
                        "email"
                    )

                    if email:

                        order.email = email

                    else:

                        order.email = (
                            request.user.email
                        )

                    # =================================================
                    # Snapshot آدرس
                    # =================================================

                    order.address = (
                        self.make_address_snapshot(
                            address
                        )
                    )

                    # =================================================
                    # ذخیره Order
                    # =================================================

                    order.save()

                    # =================================================
                    # هماهنگ کردن OrderItem با Cart
                    # =================================================

                    self.sync_order_items(
                        order,
                        cart
                    )
                    order.update_final_price()

                    # =================================================
                    # دوباره محاسبه قیمت نهایی Order
                    # =================================================

                    # order.final_price = final_price
                    #
                    # Order.objects.filter(
                    #     pk=order.pk
                    # ).update(
                    #     final_price=final_price
                    # )

                    # =================================================
                    # ذخیره Order ID در Session
                    # =================================================
                    request.session[
                        "checkout_order_id"
                    ] = order.id

                    request.session.modified = True

            # =================================================
            # خطای اطلاعات Cart / Product
            # =================================================

            except ValueError as error:

                return render(
                    request,
                    self.template_name,
                    {
                        "form1": AddressForm(),

                        "form2": form2,

                        "addresses": addresses,

                        "order": order,

                        "cart": cart,

                        "cart_total_with_discount": (
                            cart_total_with_discount
                        ),

                        "final_price": final_price,

                        "error": str(error),
                    }
                )

            # =================================================
            # Cart را پاک نمی‌کنیم
            # =================================================

            return redirect(
                "orders_cart:payment",
                order_id=order.id
            )

        # =================================================
        # درخواست نامعتبر
        # =================================================

        return redirect(
            "orders_cart:checkout"
        )


@method_decorator(login_required, name="dispatch")
class Payment(TemplateView):
    template_name = "payment.html"

    def get_context_data(self,order_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_id"] = order_id
        return context

@method_decorator(login_required, name="dispatch")
class YES(View):
    template_name = "YES.html"

    def get(self, request, order_id):
        request.session.pop(
            "checkout_order_id",
            None
        )
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user,
            status="waiting_payment",
            is_paid=False,
        )
        order.status = "awaiting_approval"
        order.is_paid = True
        order.payment_time = timezone.now()
        order.save()
        cart = Cart(request)
        cart.remove_cart()
        send_mail(
            subject="ثبت سفارش| میوکا ",
            message=f"""
                سلام {request.user.username}
                سفارش شما ثبت شد.
                کد پیگیری شما:

                {order.tracking_code}
                وضعیت تایید سفارش شما حداکثر تا 24 ساعت دیگر مشخص خواهد شد.
                شما می توانید وضعیت سفارش را از بخش سفارشات در پنل کاربری خود مشاهده کنید.
                پس از تایید سفارش ارسال محصول حداکثر تا 5 روز کاری انجام خواهد شد. 
                در صورت عدم تایید سفارش  مبلغ پرداختی فورا به حساب شما بر می گردد
                در صورت بروز مشکل می توانید از طریق قسمت ارتباط با ما یاراه های ارتباطی در بخش درباره ما با ما ارتباط بگیرید. 
                از خرید شما سپاسگزاریم:)
                میوکا


                """,
            from_email=None,
            recipient_list=[order.email],
            fail_silently=False,
        )

        # order = get_object_or_404(
        #     Order,
        #     id=order_id,
        #     user=request.user,
        # )
        return render(request, self.template_name, {"order": order})

@login_required()
def delete_add(request , pk):
    add=get_object_or_404(Address,pk=pk,user=request.user)
    add.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
@method_decorator(login_required, name="dispatch")
class OrderDetails(DetailView):
    template_name = "orders_details.html"
    context_object_name = "order"
    model = Order


@method_decorator(login_required, name="dispatch")
class OrderList(ListView):
    template_name = "orders_list.html"
    context_object_name = "orders"
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_paid=True).order_by("-payment_time")

# @method_decorator(login_required, name="dispatch")
# class Checkout(View):
#
#     template_name = "checkout.html"
#
#     def get(self, request):
#         form1 = AddressForm()
#
#         addresses = Address.objects.filter(
#             user=request.user
#         )
#
#
#         # آیا قبلاً در همین فرآیند Checkout سفارشی ساخته شده؟
#         order_id = request.session.get("checkout_order_id")
#
#         if order_id:
#             order = Order.objects.filter(
#                 id=order_id,
#                 user=request.user,
#                 status=Order.status.waiting_payment,
#             ).first()
#
#             if order:
#                 # چون Order وجود دارد،
#                 # اطلاعات قبلی را داخل فرم می‌ریزیم
#                 form2 = OrderForm(instance=order)
#
#                 return render(request, self.template_name, {
#                     "form1": form1,
#                     "form2": form2,
#                     "order": order,
#                     "addresses": addresses,
#                 })
#
#             # اگر Order پیدا نشد، Session را پاک می‌کنیم
#             request.session.pop("checkout_order_id", None)
#
#         # اولین ورود به Checkout
#         form2 = OrderForm()
#
#         return render(request, self.template_name, {
#             "form1": form1,
#             "form2": form2,
#             "addresses": addresses,
#         })
#
#
#
#
#     def post(self, request):
#         if "address" in request.POST:
#             form1 = AddressForm(request.POST)
#             form2 = OrderForm()
#
#             if form1.is_valid():
#
#                 # تعداد آدرس‌های فعلی کاربر
#                 address_count = Address.objects.filter(
#                     user=request.user
#                 ).count()
#
#                 # حداکثر ۳ آدرس
#                 if address_count >= 3:
#                     return render(request, self.template_name, {
#                         "form1": form1,
#                         "form2": form2,
#                         "addresses": Address.objects.filter(
#                             user=request.user
#                         ),
#                         "error": "شما حداکثر می‌توانید ۳ آدرس ذخیره کنید.",
#                     })
#
#                 # ساخت آدرس جدید
#                 address = form1.save(commit=False)
#                 address.user = request.user
#                 address.save()
#
#                 # دوباره آدرس‌ها را بگیر
#                 addresses = Address.objects.filter(
#                     user=request.user
#                 )
#
#                 return render(request, self.template_name, {
#                     "form1": AddressForm(),
#                     "form2": form2,
#                     "addresses": addresses,
#                 })
#
#             # اگر فرم معتبر نبود
#             addresses = Address.objects.filter(
#                 user=request.user
#             )
#
#             return render(request, self.template_name, {
#                 "form1": form1,
#                 "form2": form2,
#                 "addresses": addresses,
#             })
#         elif "payment" in request.POST:
#             form1 = AddressForm()
#             # بررسی می‌کنیم قبلاً برای این Checkout سفارش ساخته شده یا نه
#             order_id = request.session.get("checkout_order_id")
#
#             if order_id:
#
#                 order = Order.objects.filter(
#                     id=order_id,
#                     user=request.user,
#                     status=Order.status.waiting_payment,
#                 ).first()
#
#             else:
#                 order = None
#
#             # اگر Order قبلاً ساخته شده،
#             # فرم را با همان Order بررسی می‌کنیم
#             if order:
#                 form2 = OrderForm(
#                     request.POST,
#                     instance=order
#                 )
#
#             else:
#                 form2 = OrderForm(request.POST)
#
#             if not form2.is_valid():
#                 return render(request, self.template_name, {
#                     "form2": form2,
#                     "form1": form1,
#                     "order": order,
#                 })
#
#             # ---------------------------------
#             # Order را فقط یک بار ایجاد می‌کنیم
#             # ---------------------------------
#
#             if order is None:
#
#                 order = form2.save(commit=False)
#
#                 order.user = request.user
#                 order.status = Order.status.waiting_payment
#
#                 # اگر total_price را از Cart محاسبه می‌کنی
#                 # اینجا مقدارش را تعیین کن
#                 #
#                 # order.total_price = ...
#
#                 order.save()
#
#                 # Order ID را در Session نگه می‌داریم
#                 request.session["checkout_order_id"] = order.id
#
#             else:
#
#                 # Order قبلاً وجود داشته،
#                 # پس فقط اطلاعاتش را آپدیت می‌کنیم
#                 form2.save()
#
#             # ---------------------------------
#             # از اینجا به بعد Order داریم
#             # ---------------------------------
#
#             return redirect(
#                 "payment",
#                 order_id=order.id
#             )
#
#
