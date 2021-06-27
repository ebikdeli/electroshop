from django import forms
# from tinymce.widgets import TinyMCE
# from django_quill.forms import QuillFormField


class Comment(forms.Form):
    # comment = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 10, 'placeholder': 'نظر خود را وارد کنید'}))
    # comment2 = QuillFormField()
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'نظر خود را وارد کنید'}))
