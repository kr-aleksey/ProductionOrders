from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Category, Product


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    context_object_name = 'products'
    paginate_by = 20
    template_name = 'orders/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{settings.BRAND} | Каталог'
        context['categories'] = Category.objects.filter(parent=None).prefetch_related('children')
        return context

    def get_queryset(self):
        return Product.objects.all(self.request.user)
