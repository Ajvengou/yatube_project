from django.conf import settings

from django.contrib import admin

from django.urls import include, path

urlpatterns = [
    # Сначала проверяем все пути, которые есть в приложении post
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]
