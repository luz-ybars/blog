from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Post, Comentario
from .forms import ComentarioForm, ContactoForm 
from django.core.paginator import Paginator, EmptyPage
from django.core.mail import send_mail 
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def home(request):
  posts=Post.objects.all().order_by('fch_publicacion')
  return render(request, "index.html",{'posts':posts} )

def posts(request):
  posts=Post.objects.all().order_by('fch_publicacion')
  return render(request, "posts.html",{'posts':posts})

def about(request):
  return render(request, "about.html")



def post_detalle(request, id):
    """
    Muestra los detalles de un post específico, sus comentarios y maneja el formulario
    para nuevos comentarios.
    """
    post = get_object_or_404(Post, pk=id)
    comentarios = Comentario.objects.filter(post=post).order_by('-fch_creacion_comentario')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            # Crea una instancia del comentario pero no la guarda aún
            nuevo_comentario = form.save(commit=False)
            
            # Asigna el post al comentario
            nuevo_comentario.post = post
            
            # Verifica si el usuario está autenticado y asigna el autor
            if request.user.is_authenticated:
                nuevo_comentario.autor = request.user
            else:
                # Si el usuario no está autenticado, puedes manejar esto de otra forma,
                # por ejemplo, redirigiendo al login.
                messages.error(request, 'Debes iniciar sesión para comentar.')
                return redirect('auth_app:login')

            # Ahora sí, guarda el comentario en la base de datos
            nuevo_comentario.save()
            messages.success(request, 'Tu comentario ha sido enviado con éxito.')
            return redirect('post_detalle', id=post.id)
    else:
        form = ComentarioForm()

    return render(request, 'post_detalle.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form
    })


def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        comentario.delete()
        return redirect('post_detalle', id=comentario.post.id)
    return render(request, 'eliminar_comentario.html', {'comentario': comentario})


def contacto(request):
    """
    Muestra el formulario de contacto y procesa los datos enviados.
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            
        
            cuerpo_mensaje = f"Nombre: {nombre}\nEmail: {email}\n\nAsunto: {asunto}\n\nMensaje:\n{mensaje}"
            
            try:
                send_mail(
                    asunto, 
                    cuerpo_mensaje, 
                    settings.EMAIL_HOST_USER, 
                    ['tucorreo@ejemplo.com'], 
                    fail_silently=False,
                )
                messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
                return redirect('contacto')
            except Exception as e:
                messages.error(request, 'Hubo un error al enviar tu mensaje. Inténtalo de nuevo más tarde.')
                print(f"Error al enviar correo: {e}")
    else:
        form = ContactoForm()
        
    return render(request, 'contacto.html', {'form': form})



@login_required # Importante: asegura que solo usuarios autenticados puedan comentar
def nuevo_comentario(request, post_id):
    """
    Maneja la creación de un nuevo comentario para un post.
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            # No guardamos el formulario directamente.
            # Creamos una instancia del modelo pero no la guardamos todavía.
            comentario = form.save(commit=False)
            comentario.autor_comentario = request.user
            comentario.post = post
            
            
            comentario.save()
            return redirect('post_detalle', id=post.id)
    else:
      
        return redirect('post_detalle', id=post.id)

