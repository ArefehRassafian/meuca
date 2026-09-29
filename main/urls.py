
from django.urls import path
from . import views

app_name = 'main'


urlpatterns = [
    path("blog_list/",views.BlogList.as_view(),name="blog_list"),
    path("blog_details/<int:pk>",views.BlogDetails.as_view(),name="blog_details"),


    ]