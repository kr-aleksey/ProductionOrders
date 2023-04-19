from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from users.models import Counterparty, User

product_quantity_attrs = {
    'max_digits': 9,
    'decimal_places': 3,
    'validators': [MinValueValidator(0)]
}


class MeasurementUnit(models.Model):
    """
    Единицы измерения.
    """
    name = models.CharField('Наименование',
                            max_length=20,
                            unique=True)
    uid_erp = models.CharField('Идентификатор в ERP',
                               max_length=40,
                               blank=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Категории продукции.
    """
    name = models.CharField('Наименование',
                            max_length=150)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               related_name='children',
                               blank=True,
                               null=True,
                               verbose_name='Родитель')
    uid_erp = models.CharField('Идентификатор в ERP',
                               max_length=40,
                               blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):

    def in_stock(self):
        return self.filter(in_stock=True)

    def annotate_is_in_cart(self, user):
        if user.is_anonymous:
            return self.all()
        products_in_cart = Cart.objects.filter(user=user,
                                               product=models.OuterRef('pk'))
        return self.annotate(is_in_cart=models.Exists(products_in_cart))


class Product(models.Model):
    """
    Продукция.
    """
    name = models.CharField('Наименование',
                            max_length=150,
                            unique=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 verbose_name='Категория')
    counterparty = models.ForeignKey(Counterparty,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True,
                                     verbose_name='Контрагент')
    measurement_unit = models.ForeignKey(MeasurementUnit,
                                         on_delete=models.PROTECT,
                                         verbose_name='Единица измерения')
    pack_quantity = models.DecimalField(
        'Количество в упаковке',
        max_digits=8,
        decimal_places=3,
        validators=[MinValueValidator(0.001)],
        default=1
    )
    uid_erp = models.CharField('Идентификатор в ERP',
                               max_length=40,
                               blank=True,
                               null=True)
    in_stock = models.BooleanField('В продаже',
                                   default=False)

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукция'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Корзина покупок.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='products_in_cart',
                             verbose_name='Заказчик')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт')
    quantity = models.DecimalField('Количество',
                                   **product_quantity_attrs)

    class Meta:
        ordering = ('product__name',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_user_product'
            )
        ]


class Order(models.Model):
    """
    Заказы покупателей.
    """
    CANCELED = 'canceled'
    CREATED = 'created'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUSES = (
        (CANCELED, 'Отменен покупателем'),
        (CREATED, 'Создан покупателем'),
        (ACCEPTED, 'Принят исполнителем'),
        (REJECTED, 'Отклонен исполнителем'),
    )
    number = models.PositiveIntegerField('Номер')
    counterparty = models.ForeignKey(Counterparty,
                                     on_delete=models.CASCADE,
                                     related_name='orders',
                                     verbose_name='Контрагент')
    customer = models.ForeignKey(User,
                                 on_delete=models.PROTECT,
                                 related_name='orders',
                                 verbose_name='Заказчик')
    status = models.CharField('Статус',
                              max_length=20,
                              choices=STATUSES)
    created_at = models.DateTimeField('Создан',
                                      auto_now_add=True)
    note = models.TextField('Примечания',
                            blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)

    def __str__(self):
        return self.counterparty.name

    def get_absolute_url(self):
        return reverse('orders:order_update', kwargs={'pk': self.pk})

    @property
    def can_edited_by_counterparty(self):
        """
        Возвращает разрешение на изменение контрагентом.
        """
        if self.status in (self.CREATED,):
            return True
        return False


class OrderProduct(models.Model):
    """
    M2M Заказ-продукт
    """
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='products',
                              verbose_name='Заказ')
    product = models.ForeignKey('Product',
                                on_delete=models.PROTECT,
                                verbose_name='Продукт')
    quantity = models.DecimalField('Количество',
                                   **product_quantity_attrs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукция'
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_order_product'
            )
        ]

    def __str__(self):
        return self.product.name
