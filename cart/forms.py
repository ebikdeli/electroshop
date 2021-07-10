from django import forms


class ChangeCart(forms.Form):
    quantity = forms.IntegerField()


class CouponCode(forms.Form):
    promo_code = forms.CharField()
