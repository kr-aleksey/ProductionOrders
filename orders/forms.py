from django import forms

from .models import Cart
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
