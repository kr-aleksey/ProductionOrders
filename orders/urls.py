from django.urls import path

from .views import (CartListView, OrderCreateView, OrderListView,
                    OrderUpdateView, ProductListView, cart_item_view)

app_name = 'orders'

urlpatterns = [
    path('products/categories/<int:category_id>/', ProductListView.as_view()),
    path('products/categories/', ProductListView.as_view(), name='catalog'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('cart/edit/', cart_item_view, name='cart_edit'),
    path('cart/ordering/', OrderCreateView.as_view(), name='order_create'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
]
