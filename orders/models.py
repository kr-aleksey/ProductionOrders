from django.db import models

from users.models import Counterparty, User


class MeasurementUnit(models.Model):
    """
    Единицы измерения.
    """
    name = models.CharField('Наименование',
                            max_length=20)
    uid_erp = models.CharField('Идентификатор в ERP',
                               max_length=40,
                               unique=True)

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

    # uid_erp = models.CharField('Идентификатор в ERP',
    #                            max_length=40,
    #                            blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):

    def in_stock(self):
        return self.filter(in_stock=True)


class Product(models.Model):
    """
    Продукция.
    """
    name = models.CharField('Наименование',
                            max_length=150,
                            unique=True)
    measurement_unit = models.ForeignKey(MeasurementUnit,
                                         on_delete=models.PROTECT,
                                         verbose_name='Единица измерения')
    uid_erp = models.CharField('Идентификатор в ERP',
                               max_length=40,
                               unique=True)
    in_stock = models.BooleanField('В продаже',
                                   default=False)

    objects = ProductManager()

    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Заказы покупателей.
    """
    CREATED = 'created'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUSES = (
        (CREATED, 'Создан покупателем'),
        (ACCEPTED, 'Принят исполнителем'),
        (REJECTED, 'Отклонен исполнителем')
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
    note = models.TextField('Примечание',
                            blank=True)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('counterparty',)

    def __str__(self):
        return self.counterparty.name


class OrderProduct(models.Model):
    """
    M2M Заказ-номенклатура
    """
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='products',
                              verbose_name='Заказ')
    product = models.ForeignKey('Product',
                                on_delete=models.PROTECT,
                                verbose_name='Продукт')
    amount = models.DecimalField('Количество',
                                 max_digits=10,
                                 decimal_places=3)

    class Meta:
        # ordering = ('order', )
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_order_product'
            )
        ]

    def __str__(self):
        return self.product.name
