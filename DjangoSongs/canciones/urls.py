from django.urls import path
from . import views

app_name = 'canciones'  # Espacio de nombres para evitar colisiones entre apps

urlpatterns = [
    path('', views.index, name='index'),  # Ruta raíz → vista index
]