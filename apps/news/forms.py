from django import forms


class NewArticleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), max_length=255)

    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
