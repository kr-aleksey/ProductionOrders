from django import forms
from django.core.exceptions import ValidationError

from .models import Cart, Order
from .services import creat_or_update_cart_item, delete_cart_item


class CartItemForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('product', 'quantity')
        widgets = {
            'product': forms.HiddenInput,
        }

    def __init__(self, hidden=True, request=None, **kwargs):
        super().__init__(**kwargs)
        self.request = request
        if hidden:
            self.fields['quantity'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity', 0)
        if product is not None and quantity != 0:
            self.cleaned_data['quantity'] = max(quantity,
                                                product.pack_quantity)

    def save(self, commit=True):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']
        if quantity == 0:
            delete_cart_item(self.request.user, product)
            return None
        return creat_or_update_cart_item(self.request.user,
                                         product,
                                         quantity)


class OrderForm(forms.ModelForm):

    cancel = forms.BooleanField(label='Отменить заказ', required=False)

    disabled = False

    class Meta:
        model = Order
        fields = ('note', 'cancel')
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.instance.can_edited_by_counterparty:
            self.disabled = True
            self.fields['note'].disabled = True
            self.fields['cancel'].disabled = True

    def clean_cancel(self):
        cancel = self.cleaned_data['cancel']
        if cancel and not self.instance.can_edited_by_counterparty:
            raise ValidationError('Заказ в текущем статусе '
                                  'не может быть отменен.')
        return cancel

    def save(self, commit=True):
        order = super().save(commit=False)
        if self.cleaned_data.get('cancel'):
            order.status = Order.CANCELED
        order.save()
        return order
