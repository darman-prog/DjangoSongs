from django.db import models

class Cancion(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título")
    artista = models.CharField(max_length=100, verbose_name="Artista")
    album = models.CharField(max_length=100, blank=True, null=True, verbose_name="Álbum")
    duracion = models.DurationField(help_text="Formato: MM:SS", verbose_name="Duración")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Agregado")

    def __str__(self):
        return f"{self.titulo} - {self.artista}"

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Canciones"
        ordering = ['-fecha_creacion']  # Muestra primero las más recientes