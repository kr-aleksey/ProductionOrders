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
    Категории номенклатуры.
    """
    name = models.CharField('Наименование',
                            max_length=150)
    uid_erp = models.CharField('Идентификатор в ERP',
                               max_length=40,
                               unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Nomenclature(models.Model):
    """
    Номенклатура.
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

    nom = models.ManyToManyField(Nomenclature,
                                 through='OrderNomenclature')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('counterparty',)

    def __str__(self):
        return self.counterparty.name


class OrderNomenclature(models.Model):
    """
    M2M Заказ-номенклатура
    """
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='nomenclatures',
                              verbose_name='Заказ')
    nomenclature = models.ForeignKey('Nomenclature',
                                     on_delete=models.PROTECT,
                                     verbose_name='Номенклатура')
    amount = models.DecimalField('Количество',
                                 max_digits=10,
                                 decimal_places=3)

    class Meta:
        verbose_name = 'Номенклатура заказа'
        verbose_name_plural = 'Номенклатуры заказов'
        ordering = ('order', 'nomenclature')
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'nomenclature'],
                name='unique_order_nomenclature'
            )
        ]

    def __str__(self):
        return f'{self.order.number} {self.nomenclature.name}'
