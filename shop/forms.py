from django import forms


class ProductQuantity(forms.Form):
    quantity = forms.IntegerField()
