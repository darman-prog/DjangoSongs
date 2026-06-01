"""Vistas para la aplicación de canciones."""

from django.shortcuts import render
from django.http import HttpResponse
from .models import Cancion

def lista_canciones(request):
    """Traemos las canciones de MySQL y las mostramos en la tabla."""
    todas_las_canciones = Cancion.objects.all()
    
    # Renderizamos la plantilla pasándole la lista
    return render(request, 'canciones/lista.html', {'canciones': todas_las_canciones})

# ── ¡AGREGAMOS ESTA FUNCIÓN PARA SANAR EL ERROR DE LAS URLS! ─────────────────
def crear_cancion(request):
    """Vista temporal para el formulario de añadir una nueva canción."""
    return HttpResponse("¡Aquí irá el formulario para añadir música en la Fase 4!")

def editar_cancion(request, cancion_id):
    """Vista temporal para capturar el ID de la canción a editar."""
    return HttpResponse(f"¡Conectado! En la Fase 4 aquí editaremos la canción con ID: {cancion_id}")