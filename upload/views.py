from django.shortcuts import render


# Create your views here.
def upload_url(requset):
    return render(requset, "upload/upload_page.html", {})
