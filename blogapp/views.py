from django.shortcuts import render
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
