from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from .models import  Novedad

# Create your views here.
def noticia_list(request):
    """
    Vista para la lista de noticias, con funcionalidad de búsqueda.
    """
    query = request.GET.get('q')
    noticias_queryset = Novedad.objects.filter(publicado=True)

    if query:
        noticias_queryset = noticias_queryset.filter(
            Q(titulo__icontains=query) | Q (contenido__icontains=query)
        ).distinct()

    # Novedades recientes 
    ultimas_novedades = noticias_queryset.order_by('-fecha_publicacion')[:5]
    
    # Categorías y etiquetas (si existen en el modelo)
    # categorias = Categoria.objects.all()
    # etiquetas = Etiqueta.objects.all()

    context = {
        'noticias': noticias_queryset,
        'query': query,
        'ultimas_novedades': ultimas_novedades,
        # 'categorias': categorias,
        # 'etiquetas': etiquetas,
    }
    return render(request, 'noticias/lista_noticias.html', context)

def lista_noticias(request):
    query = request.GET.get('q')
    if query:
        noticias = noticias.objects.filter(publicado=True).filter(
            Q(titulo__icontains=query) | Q (contenido__icontains=query)
        ).distinct()
    else:
        noticias = noticias.objects.filter(publicado=True)

    # Novedades recientes 
    ultimas_novedades = Novedad.objects.filter(publicado=True).order_by('-fecha_publicacion')[:5]

    # Artistas destacados 
    artistas_destacados = Artista.objects.all().order_by('nombre')[:10] 

    categorias = categorias.objects.all()
    etiquetas = etiquetas.objects.all()

    context = {
        'noticias': noticias,
        'categorias': categorias,
        'etiquetas': etiquetas,
        'query': query,
        'ultimas_novedades': ultimas_novedades, 
        'artistas_destacados': artistas_destacados,
    }
    return render(request, 'noticias/lista_noticias.html', context)

