from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('analyze/', views.analyze_image, name='analyze_image'),
    path('analyze/<str:image_id>/', views.analyze_image, name='analyze_image_with_id'),
]