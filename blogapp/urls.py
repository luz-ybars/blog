from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('post_detalle/<int:id>/', views.post_detalle, name='post_detalle'),
    path('contacto/', views.contacto, name='contacto'), 
    # Esta ruta captura la clave primaria (pk) de un post y la pasa a la vista 'post_detail'.
    # El nombre de la URL es 'post_detail'.
    
    # Oras rutas que podrías necesitar para el blog
    #path('posts/', views.post_list, name='post_list'),
]

