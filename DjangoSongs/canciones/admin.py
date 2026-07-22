from django.contrib import admin
from .models import Cancion

@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'artista', 'album', 'duracion', 'tiene_youtube', 'fecha_creacion')
    search_fields = ('titulo', 'artista', 'album')
    list_filter = ('artista', 'fecha_creacion')

    def tiene_youtube(self, obj):
        return bool(obj.youtube_url)
    tiene_youtube.short_description = "YouTube"
    tiene_youtube.boolean = True