from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from smartshelf.views import startup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    path('', startup, name='startup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
