# ErroresDoc

## Error 1: Modal Template Tag

- Mensaje: `Could not parse the remainder: '(attrs={"class": "form-control dj-input", ...})'`
- Archivo: `templates/canciones/crear.html`
- Contexto: se intentó usar `{{ field.as_widget(attrs={...}) }}` para inyectar atributos en widgets.

### Por qué ocurrió

El motor de plantillas de Django no interpreta llamadas a métodos con argumentos nombrados en `{{ ... }}`.

### Solución

- Instalé `django-widget-tweaks` y lo registré en `INSTALLED_APPS`.
- Cambié la plantilla para usar `{{ field|add_class:"form-control dj-input" }}`.
- Configuré `widgets` y `label_class` en `forms.py` en lugar de en la plantilla.

---

## Error 2: Congelamiento de Modal

- Síntoma: pantalla congelada cuando se abre el modal de eliminación.
- Archivo afectado: `templates/base.html` y `templates/canciones/lista.html`
- Contexto: conflictos de z-index y pseudo-elementos fijos.

### Solución

- se quito el backdrop y se creo uno propio con css

---

## Archivos modificados

- [base.html](templates/base.html) — ajuste de z-index en pseudo-elementos
- [lista.html](templates/canciones/lista.html) — añadido `pointer-events: auto` al modal-backdrop
- [forms.py](canciones/forms.py) — configuración de widgets
- [crear.html](templates/canciones/crear.html) — uso de django-widget-tweaks

