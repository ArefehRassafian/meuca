from django.utils import timezone

from products.models import Product ,Category
from main.models import Setting




# def product_list_published(request):
#     products = Product.objects.filter(published_at__lte=timezone.now())
#     return {"products": products}

def category_list(request):
    categories = Category.objects.all()
    return {"categories": categories}

def setting(request):
    s = Setting.objects.first()
    return {"setting": s}


