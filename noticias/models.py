from django.db import models

# Create your models here.from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

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