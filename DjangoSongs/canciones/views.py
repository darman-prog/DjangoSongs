"""Vistas para la aplicación de canciones."""
from .forms import CancionForm
from django.shortcuts import redirect 
from django.shortcuts import render
from .services import song_service
# views.py
def lista_canciones(request):
    todas_las_canciones = song_service.obtener_todas_las_canciones()
    return render(request, 'canciones/lista.html', {'canciones': todas_las_canciones})

def crear_cancion(request):
    """Maneja la visualización y delega el guardado al servicio."""
    if request.method == 'POST':
        form = CancionForm(request.POST)
        if form.is_valid():
            song_service.crear_nueva_cancion(form.cleaned_data)
            return redirect('canciones:index')
    else:
        form = CancionForm()
        
    return render(request, 'canciones/crear.html', {'form': form})


def eliminar_cancion(request, cancion_id):
    """Maneja la petición de eliminación y delega la acción al servicio."""
    if request.method == 'POST':
        song_service.eliminar_cancion_por_id(cancion_id)
    
    return redirect('canciones:index')


def editar_cancion(request, cancion_id):
    cancion = song_service.obtener_cancion_por_id(cancion_id)
    
    if request.method == 'POST':
        form = CancionForm(request.POST, instance=cancion)
        if form.is_valid():
            song_service.actualizar_datos_de_cancion(cancion, form.cleaned_data)
            return redirect('canciones:index')
    else:
        form = CancionForm(instance=cancion)
        
    return render(request, 'canciones/form_cancion.html', {'form': form})