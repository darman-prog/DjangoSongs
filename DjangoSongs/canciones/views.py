from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Vista de la portada principal.
    Recibe la petición HTTP y retorna la plantilla index.html.
    """
    return render(request, 'index.html')