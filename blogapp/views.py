from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Comentario

# Create your views here.
def home(request):
  posts=Post.objects.all().order_by('fch_publicacion')
  return render(request, "index.html",{'posts':posts} )

def posts(request):
  posts=Post.objects.all().order_by('fch_publicacion')
  return render(request, "posts.html",{'posts':posts})

def postdetalle(request, id):
  try:
    data = Post.objects.get(id=id)
    comentarios = Comentario.objects.all()
  except Post.DoesNotExist:
    raise Http404('El Post seleccionado no existe')

  context ={
    "post": data,
    "comentarios": comentarios
  }

  return render(request, 'detalle_post.html',context)


def postdetalle(request, pk):
  """
    Muestra los detalles de un post, sus comentarios y maneja el formulario para nuevos comentarios.
    Permite filtrar comentarios por autor.
    """
  post = get_object_or_404(Post, pk=pk) 
  comentarios = Comentario.objects.filter(post=post) 
  autor_id = request.GET.get('autor_id')
  if autor_id:
        comentarios = comentarios.filter(autor_comentario__id=autor_id)
    
  comentarios = comentarios.order_by('-fch_creacion_comentario')
    
  if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.post = post
            nuevo_comentario.autor_comentario = request.user 
            nuevo_comentario.save()
            
            return redirect('post_detalle', pk=post.pk)
  else:
       
        form = ComentarioForm()

  context = {
        'post': post,
        'comentarios': comentarios,
        'form': form
    }
  return render(request, 'detalle_post.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from .models import Post, Comentario, Novedad, Artista, Categoria, TipoMusical, Eventos
from .forms import ComentarioForm 

# ====================================================================
# VISTAS GENERALES DEL BLOG
# ====================================================================

def home(request):
  """
  Vista de la página de inicio.
  Muestra una lista de los posts más recientes ordenados por fecha de publicación.
  """
  posts = Post.objects.all().order_by('-fch_publicacion')
  context = {
      'posts': posts
  }
  return render(request, "index.html", context)

def post_list(request):
  """
  Vista para la lista completa de posts.
  """
  posts = Post.objects.all().order_by('-fch_publicacion')
  context = {
      'posts': posts
  }
  return render(request, "posts.html", context)

def post_detail(request, pk):
    """
    Muestra los detalles de un post específico, sus comentarios y maneja el formulario para nuevos comentarios.
    Permite filtrar comentarios por autor.
    """
    post = get_object_or_404(Post, pk=pk)
    
    # Prepara la consulta base para los comentarios del post
    comentarios = Comentario.objects.filter(post=post)
    
    # Lógica para el filtrado por autor
    autor_id = request.GET.get('autor_id')
    if autor_id:
        comentarios = comentarios.filter(autor_comentario__id=autor_id)
    
    comentarios = comentarios.order_by('-fch_creacion_comentario')
    
    if request.method == 'POST':
        # Se recibe el formulario con datos
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.post = post
            # Asigna el usuario autenticado como autor del comentario
            # Nota: Esto asume que el usuario está logueado.
            nuevo_comentario.autor_comentario = request.user 
            nuevo_comentario.save()
            # Redirige a la misma página para evitar envíos duplicados
            return redirect('post_detail', pk=post.pk)
    else:
        # Si es un método GET, se crea un formulario vacío
        form = ComentarioForm()

    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form
    }
    return render(request, 'detalle_post.html', context)


# ====================================================================
# VISTAS DE NOTICIAS
# ====================================================================

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


# ====================================================================
# VISTAS DE MÚSICA Y ARTISTAS
# ====================================================================

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
    
    # Recupera novedades y productos relacionados con el artista
    novedades_artista = Novedad.objects.filter(
        artista_relacionado=artista, 
        publicado=True
    ).order_by('-fecha_publicacion')[:3]
    
    # Asegúrate de que el modelo 'Producto' exista si descomentas esta línea
    # productos_artista = Producto.objects.filter(artista=artista, disponible=True)[:3]
    
    context = {
        'artista': artista,
        'novedades_artista': novedades_artista,
        # 'productos_artista': productos_artista,
    }
    return render(request, 'musica/detalle_artista.html', context)


