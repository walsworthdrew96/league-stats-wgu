from django import forms
from .models import *


class ChampionForm(forms.ModelForm):
    # form fields go here

    def __init__(self, *args, **kwargs):
        super(ChampionForm, self).__init__(*args, **kwargs)
        # add a "form-control" class to each form input for enabling bootstrap
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Champion
        fields = ("__all__")
