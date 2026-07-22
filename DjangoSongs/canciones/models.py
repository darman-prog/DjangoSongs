from django.db import models
from .utils import extraer_youtube_id

class Cancion(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título")
    artista = models.CharField(max_length=100, verbose_name="Artista")
    album = models.CharField(max_length=100, blank=True, null=True, verbose_name="Álbum" , default="Single")
    duracion = models.DurationField(help_text="Formato: MM:SS", verbose_name="Duración")
    youtube_url = models.URLField(blank=True, null=True, verbose_name="URL de YouTube")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Agregado")

    @property
    def youtube_embed_url(self):
        if not self.youtube_url:
            return ""
        vid = extraer_youtube_id(self.youtube_url)
        return f"https://www.youtube.com/embed/{vid}" if vid else ""

    @property
    def youtube_video_id(self):
        if not self.youtube_url:
            return ""
        return extraer_youtube_id(self.youtube_url) or ""

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.youtube_url:
            if not extraer_youtube_id(self.youtube_url):
                raise ValidationError({"youtube_url": "La URL de YouTube no es válida. Debe ser del tipo youtube.com/watch?v= o youtu.be/"})

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Canciones"
        ordering = ['-fecha_creacion']  # Muestra primero las más recientes