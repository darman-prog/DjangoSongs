# 📝 Bitácora de Aprendizaje: Control de Versiones con Git & GitHub

## 📅 Registro del Suceso (Fase 2: Django)

### 📌 Resumen de la Situación
Durante el proceso de subida de la documentación correspondiente a la **Fase 2: Django**, se presentó un conflicto de sincronización de historiales entre el repositorio local y el repositorio remoto en GitHub. Para solucionar el bloqueo e imponer los nuevos cambios de la Fase 2, se ejecutó un comando destructivo (`git push --force`). 

Como consecuencia directa, **se perdieron los commits previos de la Fase 1: Fundamentos** en el historial de la nube, debido a que el historial local sobrescribió por completo la línea de tiempo del repositorio remoto.

---

### 🔍 Análisis de la Causa Raíz
El problema técnico se originó por la coexistencia de dos configuraciones de Git dentro de una misma estructura física de carpetas:
1. **Repositorio Padre (Roadmap):** El cuaderno general que rastrea el avance de todas las fases de estudio.
2. **Repositorio Hijo (DjangoSongs):** El proyecto de desarrollo independiente que contenía su propia carpeta oculta `.git`.

Al estar el proyecto de Django metido físicamente dentro de una subcarpeta del Roadmap, Git lo detectó como un *embedded repository* (repositorio incrustado). Esto generó una confusión en el rastreo de rutas de Git, bloqueando la subida correcta de los archivos de documentación y provocando el posterior "choque" de historiales.

---

### 💡 Lecciones Aprendidas y Plan de Acción
Este suceso representa un hito clave en el proceso de formación como Arquitecto de Software, dejando aprendizajes fundamentales que garantizan que **no volverá a ocurrir**:

* **Manejo Estricto de Rutas:** Git es sumamente sensible a la jerarquía de directorios. A partir de ahora, se mantendrá un control riguroso sobre dónde se ejecutan los comandos y desde dónde se indexan los archivos (`git add`).
* **Aislamiento de Archivos `.git`:** Cada vez que se avance en una nueva fase que involucre un proyecto práctico independiente, se tratará el tema de los dos archivos `.git` con extrema precaución. Nunca se deben anidar repositorios de forma directa sin usar herramientas adecuadas (como `.gitignore` o aislamiento físico completo).
* **Uso Consciente de Comandos de Fuerza:** El comando `--force` actúa como un botón nuclear que reescribe la historia. Su uso quedará restringido únicamente a escenarios controlados y repositorios individuales completamente limpios.

---

### 🛠️ Nueva Estructura Sincronizada
Para solucionar el problema de raíz, la documentación se extrajo a una carpeta unificada y libre de conflictos en la raíz del Roadmap llamada `fase-2-django-notas`. El resultado actual en el **Git Graph** muestra un árbol de commits completamente sano y listo para continuar:

* **Línea de Tiempo Unificada:** Los historiales locales y remotos se han fusionado correctamente (`Merge branch 'main'`).
* **Estructura Limpia:** Los apuntes (`InstruccionesDjango.txt`, `README.md`, `UltimateFrontend.md`, `prompt-app-django.txt`) están indexados y listos para su seguimiento sin afectar el desarrollo del código del software independiente.

---
**"Un buen programador no es el que nunca comete errores, sino el que documenta, entiende y domina la herramienta tras superar el problema."**
