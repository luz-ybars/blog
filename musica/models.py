from django.db import models
from django.utils.text import slugify

#class Artista(models.Model):
    #nombre = models.CharField(max_length=100)
    #def __str__(self):
        #return self.nombre
    # Puedes añadir más campos aquí, por ejemplo:
    # fecha_nacimiento = models.DateField(null=True, blank=True)
    # biografia = models.TextField(blank=True)
    # imagen_perfil = models.ImageField(upload_to='artistas/', null=True, blank=True) # Si la moviste de blogapp

class TipoMusical(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Ej: Rock, Pop, Jazz")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

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
    slug = models.SlugField(max_length=200, unique=True, blank=True)
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
    