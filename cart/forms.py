from django import forms


class ChangeCart(forms.Form):
    quantity = forms.IntegerField()
