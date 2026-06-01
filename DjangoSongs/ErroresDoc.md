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

### Por qué ocurrió

1. Pseudo-elementos `body::before` y `body::after` tenían `z-index: 0`, pudiendo tapar contenido.
2. El `.modal-backdrop` tenía z-index 1050 pero sin `pointer-events: auto`, limitando interactividad.
3. Los pseudo-elementos con `position: fixed` y bajo z-index causaban problemas de rendering.

### Solución

- Cambié `z-index: 0` a `z-index: -1` en los pseudo-elementos de `body` (grid y glow).
- Añadí `pointer-events: auto` y `z-index: 1050 !important` al `.modal-backdrop`.
- Mantuve `z-index: 1056` en `.modal-content` para que esté por encima del backdrop.

---

## Archivos modificados

- [base.html](templates/base.html) — ajuste de z-index en pseudo-elementos
- [lista.html](templates/canciones/lista.html) — añadido `pointer-events: auto` al modal-backdrop
- [forms.py](canciones/forms.py) — configuración de widgets
- [crear.html](templates/canciones/crear.html) — uso de django-widget-tweaks

