from django.contrib import admin
from django.urls import path, include
from blogapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Blogapp con prefijo /blog/
    path('blog/', views.home, name='home'),
    path('blog/posts', views.posts, name='posts'),
   path('blog/post-detalle/<int:id>/', views.post_detalle, name='post_detalle'), 
   path('blog/post-detalle/<int:id>', views.postdetalle, name='postdetalle'),
    
    path('auth/', include('auth_app.urls')),

    # Musica como raíz principal
    path('', include('musica.urls')),

    path('about/', views.about, name='about'),
    path('contacto/', views.contacto, name='contacto'),

    # Eliminar comentario
    path('eliminar-comentario/<int:comentario_id>/',views.eliminar_comentario, name='eliminar_comentario'),
]





