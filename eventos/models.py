from django.db import models
from django.utils.text import slugify
from django.utils import timezone

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
        ordering = ['fecha_publicacion']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.fecha_evento.strftime('%d/%m/%Y %H:%M')})"
