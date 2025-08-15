from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Comentario
from .forms import ComentarioForm
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def home(request):
  posts=Post.objects.all().order_by('fch_publicacion')
  return render(request, "index.html",{'posts':posts} )

def posts(request):
  posts=Post.objects.all().order_by('fch_publicacion')
  return render(request, "posts.html",{'posts':posts})

def about(request):
  return render(request, "about.html")

def contacto(request):
  return render(request, "contacto.html")


def post_detalle(request, id):
    """
    Muestra los detalles de un post específico, sus comentarios y maneja el formulario
    para nuevos comentarios.
    """
   
    post = get_object_or_404(Post.objects.select_related('autor'), pk=id)
    
    
    comentarios = Comentario.objects.filter(post=post).order_by('-fch_creacion_comentario')
    
    
    if request.method == 'POST':
       
        form = ComentarioForm(request.POST)
        if form.is_valid():
            
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.post = post
            
            
            if request.user.is_authenticated:
                nuevo_comentario.autor_comentario = request.user
                nuevo_comentario.save() 

                return redirect('post_detalle', id=post.id)
            else:
                
                pass
    else:
    
        form = ComentarioForm()

    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form
    }
    return render(request, 'detalle_post.html', context) 

def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        comentario.delete()
        return redirect('post_detalle', id=comentario.post.id)
    return render(request, 'eliminar_comentario.html', {'comentario': comentario})

