from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from .forms import CartItemForm
from .services import get_cart_items, get_products_for_user


class ProductListView(LoginRequiredMixin, ListView):
    context_object_name = 'products'
    template_name = 'orders/product_list.html'

    def get_queryset(self):
        return get_products_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = Category.objects.filter(parent=None)
        # .prefetch_related('children')
        context['cart_item_form'] = CartItemForm(hidden=True)
        context['brand'] = settings.BRAND
        return context


class CartListView(LoginRequiredMixin, ListView):
    context_object_name = 'cart_items'
    template_name = 'orders/cart_list.html'

    def get_queryset(self):
        return get_cart_items(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_item_form'] = CartItemForm(hidden=False)
        context['brand'] = settings.BRAND
        return context


@login_required
def cart_item_view(request):
    """
    Добавление/удаление продукта в корзине.
    """
    next_url = request.GET.get('next', 'orders:catalog')
    if request.method != 'POST':
        return HttpResponseRedirect(next_url)
    form = CartItemForm(request=request, data=request.POST)
    if form.is_valid():
        form.save()
    return HttpResponseRedirect(next_url)



