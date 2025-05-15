from django import forms


class BlogForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    is_published = forms.BooleanField(required=False)
