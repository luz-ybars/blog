from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from .models import Artista, TipoMusical

def inicio(request):
    return render(request, 'musica/inicio.html')


def artista_list(request):
    """
    Muestra una lista de todos los artistas.
    """
    artistas = Artista.objects.all().order_by('nombre')
    context = {'artistas': artistas}
    return render(request, 'musica/lista_artistas.html', context)

def artista_detail(request, slug):
    """
    Muestra los detalles de un artista específico.
    """
    artista = get_object_or_404(Artista, slug=slug)
    
   
    novedades_artista = Novedad.objects.filter(
        artista_relacionado=artista, 
        publicado=True
    ).order_by('-fecha_publicacion')[:3]
    
  
    context = {
        'artista': artista,
        'novedades_artista': novedades_artista,
        # 'productos_artista': productos_artista,
    }
    return render(request, 'musica/detalle_artista.html', context) 


def lista_artistas(request):
    artistas = Artista.objects.all().order_by('nombre')
    context = {'artistas': artistas}
    return render(request, 'musica/lista_artistas.html', context)

def detalle_artista(request, slug):
    artista = get_object_or_404(Artista, slug=slug) # Asume que Artista tiene un campo 'slug'
    # También podrías recuperar sus eventos o mercancía relacionada aquí
    novedades_artista = novedad.objects.filter(artista_relacionado=artista, publicado=True).order_by('-fecha_publicacion')[:3]
    productos_artista = Producto.objects.filter(artista=artista, disponible=True)[:3]
    context = {
        'artista': artista,
        'novedades_artista': novedades_artista,
        'productos_artista': productos_artista,
    }
    return render(request, 'musica/detalle_artista.html', context)  


