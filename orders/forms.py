from django import forms

from .models import Cart
from .services import creat_or_update_cart_item, delete_cart_item


class CartItemForm(forms.ModelForm):
    delete = forms.BooleanField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Cart
        fields = ('product', 'quantity')
        widgets = {
            'product': forms.HiddenInput,
            'quantity': forms.HiddenInput,
        }

    def __init__(self, request=None, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def save(self, commit=True):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']
        if self.cleaned_data.get('delete', False):
            delete_cart_item(self.request.user, product)
            return None
        return creat_or_update_cart_item(self.request.user,
                                         product,
                                         quantity)
