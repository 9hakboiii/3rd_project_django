from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from upload import views

app_name = "upload"

urlpatterns = [
    path("upload/", views.upload_url, name="upload_url"),
    path("initialize/", views.initialize, name="initialize"),
]

# 개발 환경에서 미디어 파일 제공
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
