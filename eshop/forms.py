from django import forms
from eshop.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('user', 'title', 'receiver', 'phone', 'state', 'city', 'address', 'postcode', 'description')

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == "user":
                self.fields[field].widget = forms.HiddenInput()
