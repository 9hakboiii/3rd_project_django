from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from urllib import request as urllib_request
from upload.models import Content
from .forms import URLImageForm


def upload_url(request):
    if request.method == "POST":
        form = URLImageForm(request.POST)
        if form.is_valid():
            # 새 Content 객체 생성 (저장은 아직)
            content = Content(user=request.user)

            # URL에서 이미지 다운로드
            image_url = form.cleaned_data["url"]
            image_name = image_url.split("/")[-1]  # URL에서 파일명 추출

            # URL에서 이미지 가져오기
            response = urllib_request.urlopen(image_url)

            # 이미지 필드에 저장
            content.url_image.save(image_name, ContentFile(response.read()), save=True)

            return redirect("upload:upload_url")  # 성공 후 같은 페이지로 리다이렉트
    else:
        form = URLImageForm()

    contents = Content.objects.all()
    return render(
        request, "upload/upload_page.html", {"contents": contents, "form": form}
    )
