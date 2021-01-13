from django import forms


CATEGORY_CHOICES = (
    ('vrc', 'VRC'),
    ('vstars', 'vSTARS'),
    ('veram', 'vERAM'),
    ('vatis', 'vATIS'),
    ('sop', 'SOP'),
    ('loa', 'LOA'),
    ('mavp', 'MAVP Agreement'),
    ('misc', 'Other')
)


class AddFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control'
        }
    ))
    file_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ), label='File Description')
    category = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=CATEGORY_CHOICES
    )
