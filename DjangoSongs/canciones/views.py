"""Vistas para la aplicación de canciones."""
import logging
from .forms import CancionForm
from django.shortcuts import redirect 
from django.shortcuts import render
from .services import song_service
from .services.spotify_client import buscar_canciones, obtener_detalle_track

logger = logging.getLogger(__name__)

# views.py
def lista_canciones(request):
    todas_las_canciones = song_service.obtener_todas_las_canciones()
    # Origin dinámico para el embed de YouTube — se calcula desde el request
    # para evitar hardcodear localhost o un dominio fijo.
    # Se pasa al template como respaldo; el JS usa window.location.origin
    # como fuente principal por ser más fiable con proxies/balanceadores.
    origin = f"{request.scheme}://{request.get_host()}"
    return render(request, 'canciones/lista.html', {
        'canciones': todas_las_canciones,
        'origin': origin,
    })

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


def buscar_canciones_spotify(request):
    query = request.GET.get('q', '').strip()
    resultados = None
    error = None

    if query:
        try:
            resultados = buscar_canciones(query)
            if resultados is None:
                error = "No se pudieron obtener resultados. Intenta de nuevo más tarde."
        except Exception as e:
            logger.exception("Error en búsqueda Spotify")
            error = "Ocurrió un error al buscar en Spotify. Verifica la conexión e intenta de nuevo."

    return render(request, 'canciones/song_search.html', {
        'resultados': resultados or [],
        'query': query,
        'error': error,
    })


def detalle_cancion_spotify(request, track_id):
    cancion = None
    error = None
    try:
        cancion = obtener_detalle_track(track_id)
        if cancion is None:
            error = "No se pudo obtener la información de la canción."
    except Exception as e:
        logger.exception("Error obteniendo detalle de track %s", track_id)
        error = "Ocurrió un error al obtener el detalle."

    return render(request, 'canciones/song_detail.html', {
        'cancion': cancion,
        'error': error,
    })