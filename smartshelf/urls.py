from django.contrib import admin
from django.urls import path, include
from smartshelf.views import home  # Import the home view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),  # Add this line to redirect the root URL to the login_register view
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)