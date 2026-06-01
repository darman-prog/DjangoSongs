from django import forms
from .models import Cancion

class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        # Le decimos qué campos queremos que aparezcan en el formulario
        fields = ['titulo', 'artista','duracion','album']
        
        # Le ponemos estilos bonitos de Bootstrap/Cyberpunk a los cuadros de texto
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control dj-input', 'placeholder': 'Ej. Street Knights'}),
            'artista': forms.TextInput(attrs={'class': 'form-control dj-input', 'placeholder': 'Ej. Tokyo Pilot'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control dj-input', 'placeholder': 'Ej. 3:45'}), 
            'album': forms.TextInput(attrs={'class': 'form-control dj-input', 'placeholder': 'Ej. Neon Genesis'}
            )}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label_cls = 'form-label text-capitalize fw-bold'
        for name, field in self.fields.items():
            setattr(field, 'label_class', label_cls)