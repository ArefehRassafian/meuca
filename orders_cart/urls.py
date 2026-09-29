
from django.urls import path
from . import views

app_name = 'orders_cart'


urlpatterns = [
    path("cart/",views.CartDetails.as_view(),name="cart_details"),
    path("cartadd/<int:pk>",views.CartAdd.as_view(),name="cart_add"),
    path("cartdel/<int:pk>/",views.CartDelete.as_view(),name="cart_del"),
    path("cartsub/<int:pk>/",views.CartSub.as_view(),name="cart_sub"),
    path("checkout/",views.Checkout.as_view(),name="checkout"),
    path("headercart/",views.HeaderCart.as_view(),name="header_cart"),
    path("payment/<int:order_id>/",views.Payment.as_view(),name="payment"),
    path("YES/<int:order_id>/",views.YES.as_view(),name="YES"),
    path("order_list/",views.OrderList.as_view(),name="order_list"),
    path("order_details/<int:pk>/",views.OrderDetails.as_view(),name="order_details"),
    path("delete_address/<int:pk>/",views.delete_add,name="delete_address"),

    ]