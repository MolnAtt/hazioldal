from django import forms
import json
from django.core.exceptions import ValidationError
from .models import Dolgozat

class DolgozatForm(forms.ModelForm):
    matrix = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 50, 'cols': 50}),
        help_text="Add meg a mátrixot ilyen formátumban: [[1.0, 2.0], [3.0, 4.0]]",
    )

    def clean_matrix(self):
        data = self.cleaned_data['matrix']
        try:
            parsed_matrix = json.loads(data)
            if not all(isinstance(row, list) and all(isinstance(x, (int, float)) for x in row) for row in parsed_matrix):
                raise ValidationError("Minden sornak listának kell lennie, és csak számokat tartalmazhat.")
            return parsed_matrix
        except json.JSONDecodeError:
            raise ValidationError("A megadott adat nem érvényes formátumú.")

    class Meta:
        model = Dolgozat
        fields = '__all__'
