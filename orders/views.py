from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import CartItemForm, OrderForm
from .filters import ProductFilter
from .models import Category, Order
from .services import (create_order_from_cart, get_cart_items,
                       get_products_for_user)


class ProductListView(LoginRequiredMixin, ListView):
    context_object_name = 'products'
    template_name = 'orders/product_list.html'
    paginate_by = 15
    filter_set = None

    def get_queryset(self):
        queryset = get_products_for_user(self.request.user)
        self.filter_set = ProductFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['categories'] = (Category
        #                          .objects
        #                          .filter(parent=None)
        #                          .prefetch_related('children'))

        context['brand'] = settings.BRAND
        context['title'] = 'Каталог'
        context['filter'] = self.filter_set
        context['cart_item_form'] = CartItemForm(hidden=True)
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
        context['title'] = 'Корзина'
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
        context['title'] = 'Оформление заказа'
        return context

    def form_valid(self, form):
        order = create_order_from_cart(self.request.user,
                                       form.cleaned_data['note'])
        return redirect('orders:order_list')


class OrderListView(LoginRequiredMixin, ListView):
    """
    История заказов
    """
    model = Order
    context_object_name = 'orders'
    template_name = 'orders/order_list.html'
    paginate_by = 15

    def get_queryset(self):
        return (self
                .request
                .user
                .counterparty
                .orders
                .prefetch_related('customer'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = settings.BRAND
        context['title'] = 'История заказов'
        return context


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование заказа.
    """
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_update.html'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = settings.BRAND
        context['title'] = 'Детали заказа'
        context['order_items'] = (self
                                  .object
                                  .products
                                  .select_related('product__measurement_unit'))
        return context

    def get_object(self, queryset=None):
        order = get_object_or_404(Order
                                  .objects
                                  .select_related('customer', 'counterparty'),
                                  pk=self.kwargs.get('pk'))
        if order.counterparty != self.request.user.counterparty:
            raise PermissionDenied
        return order
