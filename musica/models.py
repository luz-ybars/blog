from django.db import models

# Create your models here.

class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    # Puedes añadir más campos aquí, por ejemplo:
    # fecha_nacimiento = models.DateField(null=True, blank=True)
    # biografia = models.TextField(blank=True)
    # imagen_perfil = models.ImageField(upload_to='artistas/', null=True, blank=True) # Si la moviste de blogapp

    def __str__(self):
        return self.nombre

    