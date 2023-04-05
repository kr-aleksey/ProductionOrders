# Generated by Django 4.1.7 on 2023-04-04 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('orders', '0004_alter_product_uid_erp'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='counterparty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.counterparty', verbose_name='Контрагент'),
        ),
    ]
