from django.urls import path
from . import views

app_name = 'canciones' 

urlpatterns = [
    path('', views.lista_canciones, name='index'), 
    path('crear/', views.crear_cancion, name='create'), 
    path('editar/<int:cancion_id>/', views.editar_cancion, name='update'),
    path('eliminar/<int:cancion_id>/', views.eliminar_cancion, name='delete'),
]