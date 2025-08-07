from django.contrib import admin
from django.urls import path, include
from blogapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Blogapp con prefijo /blog/
    path('blog/', views.home, name='home'),
    path('blog/posts', views.posts, name='posts'),
    path('blog/post-detalle/<int:id>', views.postdetalle, name='postdetalle'),

    # Auth
    path('auth/', include('auth_app.urls')),

    # Musica como raíz principal
    path('', include('musica.urls')),
]
