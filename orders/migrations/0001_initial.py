# Generated by Django 4.1.7 on 2023-04-01 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('uid_erp', models.CharField(max_length=40, unique=True, verbose_name='Идентификатор в ERP')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='MeasurementUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Наименование')),
                ('uid_erp', models.CharField(max_length=40, unique=True, verbose_name='Идентификатор в ERP')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Наименование')),
                ('uid_erp', models.CharField(max_length=40, unique=True, verbose_name='Идентификатор в ERP')),
                ('in_stock', models.BooleanField(default=False, verbose_name='В продаже')),
                ('measurement_unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.measurementunit', verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Продукция',
                'verbose_name_plural': 'Продукция',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер')),
                ('status', models.CharField(choices=[('created', 'Создан покупателем'), ('accepted', 'Принят исполнителем'), ('rejected', 'Отклонен исполнителем')], max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('note', models.TextField(blank=True, verbose_name='Примечание')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='users.counterparty', verbose_name='Контрагент')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('counterparty',),
            },
        ),
        migrations.CreateModel(
            name='OrderNomenclature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Количество')),
                ('nomenclature', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.nomenclature', verbose_name='Номенклатура')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nomenclatures', to='orders.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Номенклатура заказа',
                'verbose_name_plural': 'Номенклатуры заказов',
                'ordering': ('order', 'nomenclature'),
            },
        ),
        migrations.AddField(
            model_name='order',
            name='nom',
            field=models.ManyToManyField(through='orders.OrderNomenclature', to='orders.nomenclature'),
        ),
        migrations.AddConstraint(
            model_name='ordernomenclature',
            constraint=models.UniqueConstraint(fields=('order', 'nomenclature'), name='unique_order_nomenclature'),
        ),
    ]