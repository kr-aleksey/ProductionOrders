from django.urls import path

from .views import ProductListView

app_name = 'orders'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list')
]
