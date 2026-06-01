# ErroresDoc

## Error detectado

- Mensaje: `Could not parse the remainder: '(attrs={"class": "form-control dj-input", "required": "required", "id": field.id_for_label })' from 'field.as_widget(attrs={"class": "form-control dj-input", "required": "required", "id": field.id_for_label })'`
- Archivo: `templates/canciones/crear.html`
- Contexto: se intentó usar `{{ field.as_widget(attrs={...}) }}` en un template de Django para inyectar atributos de HTML en los widgets de formulario.

## Por qué ocurrió

- El motor de plantillas de Django no interpreta llamadas a métodos con argumentos nombrados dentro de `{{ ... }}`.
- La sintaxis `field.as_widget(attrs={...})` no es válida en el template de Django.
- Por esa razón, el parser no pudo entender el resto de la expresión y lanzó el error.

## Solución aplicada

1. Se instaló y configuró `django-widget-tweaks`:
   - `pip install django-widget-tweaks`
   - Agregar `widget_tweaks` en `INSTALLED_APPS` dentro de `django_songs/settings.py`.

2. Se cambió la plantilla `templates/canciones/crear.html`:
   - Se añadió `{% load widget_tweaks %}` al inicio.
   - Se reemplazó la llamada inválida por:
     ```django
     {{ field|add_class:"form-control dj-input" }}
     ```
   - Esto aplica la clase CSS al campo sin necesidad de usar `as_widget(attrs=...)`.

3. Se mantuvo la configuración de widgets base en `canciones/forms.py` usando `widgets = {...}` para `titulo` y `artista`.

4. Para las etiquetas (`<label>`), se dejó la generación explícita usando:
   ```django
   <label for="{{ field.id_for_label }}" class="{{ field.field.label_class }}">{{ field.label }}</label>
   ```
   y se asignó `label_class` desde el `Form` en `canciones/forms.py`.

## Qué tener en cuenta si vuelve a pasar

- En templates de Django, no uses sintaxis Python compleja dentro de `{{ }}`.
- Para modificar atributos de widgets desde el template, usa `django-widget-tweaks` o define los atributos en el `Form`.
- Para clases de etiqueta o estilos de label, es preferible gestionarlos en el formulario (`forms.py`) o renderizar la etiqueta explícitamente.

## Archivos modificados

- `templates/canciones/crear.html`
- `canciones/forms.py`
- `django_songs/settings.py`
