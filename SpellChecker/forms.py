from django import forms
from SpellChecker.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'description', 'document',)
