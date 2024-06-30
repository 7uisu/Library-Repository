from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', include('app.urls')),    # Include your app's URLs at the root level
    path('select2/', include('django_select2.urls')),  # Include django_select2 URLs
]

if settings. DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)