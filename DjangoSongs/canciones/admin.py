from django.contrib import admin
from .models import Cancion

@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'artista', 'album', 'duracion', 'fecha_creacion')
    search_fields = ('titulo', 'artista', 'album')
    list_filter = ('artista', 'fecha_creacion')