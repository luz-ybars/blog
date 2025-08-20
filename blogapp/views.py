from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comentario, Autor
from .forms import ComentarioForm, ContactoForm, PostForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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
          getattr(settings, 'EMAIL_HOST_USER', None) or email,
          ['tucorreo@ejemplo.com'],
          fail_silently=False,
        )
        messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
        return redirect('contacto')
      except Exception:
        messages.error(request, 'Hubo un error al enviar tu mensaje. Inténtalo de nuevo más tarde.')
  else:
    form = ContactoForm()
  return render(request, "contacto.html", { 'form': form })


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
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.post = post
            if request.user.is_authenticated:
                nuevo_comentario.autor_comentario = request.user
                nuevo_comentario.save()
            else:
                messages.error(request, 'Debes iniciar sesión para comentar.')
                return redirect('auth:login')
            messages.success(request, 'Tu comentario ha sido enviado con éxito.')
            return redirect('post_detalle', id=post.id)
    else:
        form = ComentarioForm()

    return render(request, 'post_detalle.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form
    })


def postdetalle(request, id):
    return post_detalle(request, id)

def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        comentario.delete()
        return redirect('post_detalle', id=comentario.post.id)
    return render(request, 'eliminar_comentario.html', {'comentario': comentario})

def _es_colaborador(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Colaborador').exists())

def _autor_para(user):
    nombre = user.get_full_name() or user.username
    email = user.email or f'{user.username}@example.com'
    autor, _ = Autor.objects.get_or_create(user=user, defaults={'nombre': nombre, 'email': email})
    return autor

@login_required
def post_crear(request):
    if not _es_colaborador(request.user):
        messages.error(request, 'No tenés permisos para crear artículos.')
        return redirect('posts')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = _autor_para(request.user)
            post.fch_publicacion = timezone.now()
            post.save()
            form.save_m2m()
            messages.success(request, 'Artículo creado correctamente.')
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'titulo': 'Nuevo artículo'})

@login_required
def post_editar(request, id):
    if not _es_colaborador(request.user):
        messages.error(request, 'No tenés permisos para editar artículos.')
        return redirect('posts')
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado correctamente.')
            return redirect('posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'titulo': 'Editar artículo'})

@login_required
def post_eliminar(request, id):
    if not _es_colaborador(request.user):
        messages.error(request, 'No tenés permisos para eliminar artículos.')
        return redirect('posts')
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Artículo eliminado.')
        return redirect('posts')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
