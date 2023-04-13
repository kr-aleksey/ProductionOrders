from django.urls import path

from .views import (CartListView,
                    OrderCreateView,
                    ProductListView,
                    cart_item_view)

app_name = 'orders'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='catalog'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('cart/edit/', cart_item_view, name='cart_edit'),
    path('cart/ordering/', OrderCreateView.as_view(), name='order_create'),
]
