from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mainpage.urls")),
    path("accounts/", include("accounts.urls")),
    path("upload/", include("upload.urls")),
    path('analysis/', include('analysis.urls', namespace='analysis')),
    path('game/', include('game.urls', namespace='game')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
