from django.urls import path
from upload import views

app_name = "upload"

urlpatterns = [
    path("upload/", views.upload_url, name="upload_url"),
]
