from django import forms


EMAIL_DISTRO_LISTS = (
    (0, 'All Controllers'),
    (1, 'Home Controllers'),
    (2, 'Visiting Controllers'),
    (3, 'MAVP Controllers'),
    (4, 'ARTCC Staff'),
    (5, 'Training Staff'),
    (6, 'Instructors'),
    (7, 'Mentors'),
    (8, 'S1s and above'),
    (9, 'S2s and above'),
    (10, 'S3s and above'),
    (11, 'C1s and above')
)


class SendEmailForm(forms.Form):
    subject = forms.CharField(label='Subject', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    distro = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=EMAIL_DISTRO_LISTS,
        label='Distribution List'
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}))
