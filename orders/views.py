from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView

from .forms import CartItemForm
from .models import Product
from .services import get_products_for_user


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    context_object_name = 'products'
    paginate_by = 10
    template_name = 'orders/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = settings.BRAND
        # context['categories'] = Category.objects.filter(parent=None)
        # .prefetch_related('children')
        context['cart_item_form'] = CartItemForm()
        return context

    def get_queryset(self):
        return get_products_for_user(self.request.user)


@require_POST
@login_required
def cart_edit_view(request):
    form = CartItemForm(request=request, data=request.POST)
    if form.is_valid():
        form.save()
    return redirect(request.GET.get('next'))
