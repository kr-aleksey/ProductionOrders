from django.urls import path

from .views import ProductListView, cart_edit_view

app_name = 'orders'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/add_to_cart/', cart_edit_view, name='cart_edit')
]
