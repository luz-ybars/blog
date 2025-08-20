from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blogapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('blog/', views.home, name='home'),
    path('blog/posts', views.posts, name='posts'),
    path('blog/post-detalle/<int:id>/', views.post_detalle, name='post_detalle'),
    path('blog/post-detalle/<int:id>', views.postdetalle, name='postdetalle'),
    path('blog/nuevo-post/', views.post_crear, name='post_crear'),
    path('blog/editar-post/<int:id>/', views.post_editar, name='post_editar'),
    path('blog/eliminar-post/<int:id>/', views.post_eliminar, name='post_eliminar'),
    path('auth/', include('auth_app.urls')),
    path('', views.home),
    path('about/', views.about, name='about'),
    path('contacto/', views.contacto, name='contacto'),
    path('eliminar-comentario/<int:comentario_id>/',views.eliminar_comentario, name='eliminar_comentario'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

