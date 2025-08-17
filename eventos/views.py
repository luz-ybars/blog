from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from .models import Eventos



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

    # Novedades recientes (ejemplo)
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

