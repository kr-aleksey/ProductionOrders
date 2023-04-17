from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .forms import CartItemForm
from .models import Order
from .services import (create_order_from_cart,
                       get_cart_items,
                       get_counterparty_orders,
                       get_products_for_user)


class ProductListView(LoginRequiredMixin, ListView):
    context_object_name = 'products'
    template_name = 'orders/product_list.html'
    paginate_by = 15

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
    paginate_by = 15

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


class OrderCreateView(LoginRequiredMixin, CreateView):
    """
    Оформление заказа
    """
    model = Order
    template_name = 'orders/order_create.html'
    fields = ('note',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = settings.BRAND
        return context

    def form_valid(self, form):
        order = create_order_from_cart(self.request.user,
                                       form.cleaned_data['note'])
        return HttpResponseRedirect(self.get_success_url())


class OrderListView(LoginRequiredMixin, ListView):
    """
    История заказов
    """
    model = Order
    context_object_name = 'orders'
    template_name = 'orders/order_list.html'
    paginate_by = 15

    def get_queryset(self):
        return get_counterparty_orders(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = settings.BRAND
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Заказ
    """
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = settings.BRAND
        return context

    def get_object(self, queryset=None):
        order = super().get_object()
        if order.counterparty != self.request.user.counterparty:
            raise PermissionDenied
        return order
