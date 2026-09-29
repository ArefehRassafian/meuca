
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path("product_list/",views.product_list,name="product_list"),
    path("product_details/<int:pk>",views.ProductDetails.as_view(),name="product_details"),
    path('', views.WithoutEntering.as_view(), name='without_entering'),
    path("discounted_products_list/",views.DiscountedProductsList,name="discounted_products_list"),
    path("categories_list/<int:pk>",views.CategoriesList,name="categories_list"),



    ]