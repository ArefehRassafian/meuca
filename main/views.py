from django.shortcuts import render
from django.views.generic import DetailView, ListView

from main.models import Blog


# Create your views here.

class BlogDetails(DetailView):
    template_name = "blog_details.html"
    context_object_name = "blog"
    model = Blog



class BlogList(ListView):
    template_name = "blog_list.html"
    context_object_name = "blogs"
    model = Blog
