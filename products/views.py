from decimal import Decimal

from django.core.paginator import Paginator
from django.db.models import Q, ExpressionWrapper, F, Value, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, TemplateView

from .models import Product


def product_list(request):

    p = Product.objects.filter(
        published_at__lte=timezone.now()
    )

    # جستجو
    q = request.GET.get('search', '').strip()

    if q:
        p = p.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(code__icontains=q)
        )

    # دسته‌بندی
    clist = request.GET.getlist('categories')

    if clist:
        p = p.filter(
            categories__id__in=clist
        ).distinct()

    # مرتب‌سازی
    order = request.GET.get('order')

    if order in ['2', '3']:

        p = p.annotate(
            calculated_final_price=ExpressionWrapper(
                F('price') * (
                    Value(Decimal('100')) -
                    Coalesce(
                        F('discount_percent'),
                        Value(Decimal('0'))
                    )
                ) / Value(Decimal('100')),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2
                )
            )
        )

    if order == '2' :
        p = p.order_by('calculated_final_price')
    elif order == '3':
        p = p.order_by('-calculated_final_price')



    # صفحه‌بندی
    page_num = request.GET.get('page')

    paginator = Paginator(p, 15)
    object_list = paginator.get_page(page_num)

    return render(
        request,
        "product_list.html",
        {
            'ps': object_list,
            'selected_categories': [int(x) for x in clist],
        }
    )


class ProductDetails (DetailView):
    template_name = "product_details.html"
    model = Product

class WithoutEntering(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = Product.objects.filter(published_at__lte=timezone.now(), discount_percent__gt=1).order_by(
            "-discount_percent")[:7]
        p = Product.objects.filter(published_at__lte=timezone.now()).order_by("-published_at")[:7]
        context["discounted_products"] = d
        context["products"] = p
        return context


def DiscountedProductsList(request):

    p = Product.objects.filter(
        published_at__lte=timezone.now()
    )

    # جستجو
    q = request.GET.get('search', '').strip()

    if q:
        p = p.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(code__icontains=q)
        )

    # صفحه‌بندی
    page_num = request.GET.get('page')

    paginator = Paginator(p, 50)
    object_list = paginator.get_page(page_num)

    return render(
        request,
        "products_list2.html",
        {
            'ps': object_list,

        }
    )
def CategoriesList(request , pk):

    p = Product.objects.filter(
        published_at__lte=timezone.now()
    )

    # جستجو
    q = request.GET.get('search', '').strip()

    if q:
        p = p.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(code__icontains=q)
        )

    # دسته‌بندی


    p = p.filter(
        categories__id= pk
    ).distinct()


    # صفحه‌بندی
    page_num = request.GET.get('page')

    paginator = Paginator(p, 50)
    object_list = paginator.get_page(page_num)

    return render(
        request,
        "products_list2.html",
        {
            'ps': object_list,

        }
    )