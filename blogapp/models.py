from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify 

# Create your models here.
class Autor(models.Model):
   id_autor = models.BigAutoField(primary_key=True)
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   nombre = models.CharField(max_length=100)
   email = models.EmailField(unique=True)
   biografia = models.TextField(blank=True, null=True)

   def __str__(self):
      return self.nombre

class Categoria(models.Model):
   nombre = models.CharField(max_length=300)


class Post(models.Model):
  autor=models.ForeignKey("Autor", on_delete=models.CASCADE)
  titulo = models.CharField(max_length=200)
  contenido = models.TextField()
  fch_creacion = models.DateTimeField(default=timezone.now)
  fch_publicacion = models.DateTimeField(blank=True, null=True)

  categorias = models.ManyToManyField(Categoria, related_name="posts", blank=True)

  def __str__(self):
      return self.titulo


  def publicar_articulo(self):
     self.fch_publicacion=timezone.now
     self.save()

class Comentario(models.Model):
   #autor_comentario=models.Charfield(max_lenght=60)
   autor_comentario = models.ForeignKey(User, on_delete=models.CASCADE)
   contenido_comentario = models.TextField()
   fch_creacion_comentario = models.DateTimeField(default=timezone.now)
   post = models.ForeignKey("Post",related_name="comentarios", on_delete=models.CASCADE)


   comentario_padre=models.ForeignKey(
      "self",
      null=True,
      blank=True,
      on_delete=models.CASCADE,
      related_name="respuestas"
  )

   def __str__(self):
    return f"{self.autor_comentario} - {self.contenido_comentario[:30]}"

def lista_noticias(request):
    query = request.GET.get('q')
    if query:
        noticias = Noticia.objects.filter(publicado=True).filter(
            Q(titulo__icontains=query) | Q (contenido__icontains=query)
        ).distinct()
    else:
        noticias = Noticia.objects.filter(publicado=True)

    # Novedades recientes (ejemplo)
    ultimas_novedades = Novedad.objects.filter(publicado=True).order_by('-fecha_publicacion')[:5]

    # Artistas destacados (ejemplo)
    artistas_destacados = Artista.objects.all().order_by('nombre')[:10] # Mostrar algunos artistas

    categorias = Categoria.objects.all()
    etiquetas = Etiqueta.objects.all()

    context = {
        'noticias': noticias,
        'categorias': categorias,
        'etiquetas': etiquetas,
        'query': query,
        'ultimas_novedades': ultimas_novedades, # Añade las novedades al contexto
        'artistas_destacados': artistas_destacados, # Añade los artistas al contexto
    }
    return render(request, 'noticias/lista_noticias.html', context)

# Puedes crear nuevas vistas específicas para cada tipo de contenido
def lista_artistas(request):
    artistas = Artista.objects.all().order_by('nombre')
    context = {'artistas': artistas}
    return render(request, 'musica/lista_artistas.html', context)

def detalle_artista(request, slug):
    artista = get_object_or_404(Artista, slug=slug) # Asume que Artista tiene un campo 'slug'
    # También podrías recuperar sus eventos o mercancía relacionada aquí
    novedades_artista = Novedad.objects.filter(artista_relacionado=artista, publicado=True).order_by('-fecha_publicacion')[:3]
    productos_artista = Producto.objects.filter(artista=artista, disponible=True)[:3]
    context = {
        'artista': artista,
        'novedades_artista': novedades_artista,
        'productos_artista': productos_artista,
    }
    return render(request, 'musica/detalle_artista.html', context)

# De manera similar para Novedades (detalle), Productos (lista y detalle), etc.

class TipoMusical(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Ej: Rock, Pop, Jazz")
    slug = models.SlugField(max_length=100, unique=True, blank=True) # Para URLs amigables

    class Meta:
        verbose_name = "Tipo Musical"
        verbose_name_plural = "Tipos Musicales"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Artista(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True) # Para URLs amigables
    biografia = models.TextField(blank=True, null=True)
    imagen_perfil = models.ImageField(upload_to='artistas_imagenes/', blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    tipos_musicales = models.ManyToManyField(TipoMusical, related_name='artistas', blank=True)

    class Meta:
        verbose_name = "Artista"
        verbose_name_plural = "Artistas"
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Eventos(models.Model):
    nombre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='fecha_evento', blank=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_evento = models.DateTimeField() 
    lugar = models.CharField(max_length=200) 
    direccion = models.CharField(max_length=250, blank=True, null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now) 
    imagen_evento = models.ImageField(upload_to='eventos_imagenes/', blank=True, null=True) 
    artistas_participantes = models.ManyToManyField(
        'musica.Artista', 
        related_name='eventos_participados',
        blank=True
    )
    activo = models.BooleanField(default=True, help_text="Indica si el evento está activo para venta de entradas")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['fecha_publicacion'] # Order by date, earliest first

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.fecha_evento.strftime('%d/%m/%Y %H:%M')})"
    

    class Novedad(models.Model):
     titulo = models.CharField(max_length=250)
     slug = models.SlugField(max_length=250, unique_for_date='fecha_publicacion', blank=True)
     contenido = models.TextField()
     autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='novedades_creadas')
     fecha_creacion = models.DateTimeField(auto_now_add=True) 
     fecha_publicacion = models.DateTimeField(default=timezone.now) 
     imagen_destacada = models.ImageField(upload_to='novedades_imagenes/', blank=True, null=True)
     publicado = models.BooleanField(default=False) 
     artista_relacionado = models.ForeignKey(
          'musica.Artista', 
           on_delete=models.SET_NULL, 
           null=True, blank=True,
           related_name='novedades' 
    )

    class Meta:
        verbose_name = "Novedad"
        verbose_name_plural = "Novedades"
        ordering = ['-fecha_publicacion'] 

def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

def __str__(self):
 return self.titulo  

