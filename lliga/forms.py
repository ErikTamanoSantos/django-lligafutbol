from django import forms
from .models import Equip

class CrearEquipForm(forms.ModelForm):
    class Meta:
        model = Equip
        fields = ['nom', 'lligues']