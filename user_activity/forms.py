from django import forms
from tinymce.widgets import TinyMCE


class Comment(forms.Form):
    comment = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 5}))
