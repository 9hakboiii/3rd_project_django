from django.shortcuts import render
from upload.views import upload_url


# Create your views here.
def home(request):
    return render(request, "main/mainpage.html", {})
