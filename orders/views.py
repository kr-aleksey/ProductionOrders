from django.views.generic.list import ListView

from django.conf import settings
from .models import Category, Product


class ProductListView(ListView):

    model = Product
    paginate_by = 20
    template_name = 'orders/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{settings.BRAND} | Каталог'
        context['categories'] = Category.objects.filter(parent=None).prefetch_related('children')
        return context
