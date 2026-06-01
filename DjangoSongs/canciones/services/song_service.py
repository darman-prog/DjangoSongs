# services/song_service.py
from django.shortcuts import get_object_or_404
from ..models import Cancion

#Funciones para obtener las canciones
def obtener_todas_las_canciones():
    """
    Trae todo el catálogo de canciones desde MySQL ordenado de 
    forma predeterminada.
    """
    return Cancion.objects.all() .order_by('id')

def obtener_cancion_por_id(cancion_id):
    """Busca la canción de forma segura."""
    return get_object_or_404(Cancion, id=cancion_id)

def actualizar_datos_de_cancion(cancion_instancia, datos_formulario):
    """Ejecuta las reglas de negocio y guarda en la base de datos."""
    cancion_instancia.titulo = datos_formulario.get('titulo')
    cancion_instancia.artista = datos_formulario.get('artista')
    cancion_instancia.duracion = datos_formulario.get('duracion')
    cancion_instancia.save()
    return cancion_instancia

#Funciones de crear y elimnar y editar canciones
def crear_nueva_cancion(datos_limpios):
    """
    Recibe un diccionario con los datos ya validados del formulario
    y se encarga de dar el alta real en MySQL.
    """
    # Usamos ** para desempaquetar el diccionario (titulo=valor, artista=valor...)
    cancion = Cancion.objects.create(**datos_limpios)
    return cancion

def eliminar_cancion_por_id(cancion_id):
    """
    Busca la canción de forma segura y la elimina de la base de datos.
    Si no existe, el chef maneja el error 404 de inmediato.
    """
    cancion = get_object_or_404(Cancion, id=cancion_id)
    cancion.delete()
    return True

def editar_cancion(cancion_id, datos_limpios):
    """
    Busca la canción de forma segura, actualiza sus datos y la guarda.
    Si no existe, el chef maneja el error 404 de inmediato.
    """
    cancion = get_object_or_404(Cancion, id=cancion_id)
    cancion.titulo = datos_limpios.get('titulo')
    cancion.artista = datos_limpios.get('artista')
    cancion.duracion = datos_limpios.get('duracion')
    cancion.album = datos_limpios.get('album')
    cancion.save()
    return cancion