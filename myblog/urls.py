from django.contrib import admin
from django.urls import path, include
from blogapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Blogapp con prefijo /blog/
    path('', include('blogapp.urls')),
     path('auth/', include('auth_app.urls')),
    path('about/', views.about, name='about'),
    path('contacto/', views.contacto, name='contacto'),
    path('eliminar-comentario/<int:comentario_id>/',views.eliminar_comentario, name='eliminar_comentario'),
    #path('musica/', include('musica.urls')),
    #path('eventos/', include('eventos.urls')),

    #path('blog/', views.home, name='home'),
    #path('blog/posts', views.posts, name='posts'),
    #path('blog/post-detalle/<int:id>/', views.post_detalle, name='post_detalle'), 

    #path('blog/nuevo-post/', views.nuevo_post, name='nuevo_post'),
    #path('blog/editar-post/<int:id>/', views.editar_post, name='editar_post'),
    #path('blog/eliminar-post/<int:id>/', views.eliminar_post, name='eliminar_post'),
    #path('blog/comentario/<int:post_id>/', views.comentario, name='comentario'),
    #path('blog/nuevo-comentario/<int:post_id>/', views.nuevo_comentario, name='nuevo_comentario'),
    #path('blog/editar-comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),

]



