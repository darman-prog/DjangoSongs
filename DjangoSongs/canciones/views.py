"""Vistas para la aplicación de canciones."""

from django.http import HttpResponse
from .models import Cancion
from .forms import CancionForm
from django.shortcuts import redirect , get_object_or_404
from django.shortcuts import render

def lista_canciones(request):
    """Traemos las canciones de MySQL y las mostramos en la tabla."""
    todas_las_canciones = Cancion.objects.all()
    
    # Renderizamos la plantilla pasándole la lista
    return render(request, 'canciones/lista.html', {'canciones': todas_las_canciones})

def crear_cancion(request):
    """Maneja la visualización y el guardado del formulario de una nueva canción."""
    if request.method == 'POST':
        # Si nos enviaron el formulario relleno, se lo pasamos a Django para que lo procese
        form = CancionForm(request.get_full_path_or_post_data() if hasattr(request, 'get_full_path_or_post_data') else request.POST)
        if form.is_valid():
            form.save() # ¡LA MAGIA: Guarda directo en MySQL!
            return redirect('canciones:index') # Nos regresa automáticamente al catálogo
    else:
        # Si solo entraron a mirar la página, creamos el formulario vacío
        form = CancionForm()
        
    # Le pasamos el formulario al HTML para que lo dibuje
    return render(request, 'canciones/crear.html', {'form': form})

def editar_cancion(request, cancion_id):
    """Vista temporal para capturar el ID de la canción a editar."""
    return HttpResponse(f"¡Conectado! En la Fase 4 aquí editaremos la canción con ID: {cancion_id}")



def eliminar_cancion(request, cancion_id):
    """Busca una canción por su ID y la borra de la base de datos."""
    # get_object_or_404 es un truco de seguridad: si el ID no existe, muestra un error 404 en vez de romper el servidor
    cancion = get_object_or_404(Cancion, id=cancion_id)
    
    # ¡Aquí es donde ocurre la eliminación real en MySQL!
    if request.method == 'POST':
        cancion.delete()
    
    # Una vez borrada, regresamos de inmediato al catálogo actualizado
    return redirect('canciones:index')