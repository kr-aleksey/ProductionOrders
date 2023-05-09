import django_filters

from orders.models import Product


class ProductFilter(django_filters.FilterSet):

    search = django_filters.CharFilter(field_name='name',
                                       lookup_expr='icontains',
                                       label='Поиск по наименованию')

    class Meta:
        model = Product
        fields = ('search',)
