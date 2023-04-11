from django.urls import path

from .views import CartListView, ProductListView, cart_item_view

app_name = 'orders'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='catalog'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('cart_edit/', cart_item_view, name='cart_edit'),

]
