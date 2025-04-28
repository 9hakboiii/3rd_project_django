from django.shortcuts import render
from django.core.files.base import ContentFile
from django.http import JsonResponse
from urllib import request as urllib_request
from upload.models import Content
from .forms import URLImageForm
from django.template.loader import render_to_string
from upload.upload import Upload
from django.conf import settings

# 비회원 최대 업로드 횟수 상수
MAX_NONMEMBER_UPLOADS = 5


def upload_url(request):
    form = URLImageForm(request.POST or None)
    last_uploaded_image = None
    is_upload = False

    # 세션에서 비회원 업로드 기록(dict) 가져오기
    nonmember_dict = request.session.get(settings.UPLOAD_SESSION_ID, {})

    # 사용한 횟수, 남은 횟수 계산
    used_count = len(nonmember_dict)

    # 게임에서 얻은 추가 코인 반영
    additional_coin = request.session.get('additional_coin', 0)

    coin = max(0, MAX_NONMEMBER_UPLOADS - used_count + additional_coin)
    limit_exceeded = coin <= 0

    if request.method == "POST" and form.is_valid():
        image_url = form.cleaned_data["url"]

        # 비회원 업로드 제한 체크
        if not request.user.is_authenticated and limit_exceeded:

            # 더 이상 업로드 불가
            return render(
                request,
                "upload/upload_page.html",
                {
                    "form": form,
                    "last_uploaded_image": None,
                    "is_upload": False,
                    "coin": coin,
                    "limit_exceeded": True,
                },
            )

        try:
            if request.user.is_authenticated:
                # 새 Content 객체 생성 (저장은 아직)
                content = Content(user=request.user)

                # URL에서 이미지 가져오기
                response = urllib_request.urlopen(image_url)

                # 이미지 이름 추출
                image_name = image_url.split("/")[-1]

                # 이미지 필드에 저장
                content.url_image.save(
                    image_name, ContentFile(response.read()), save=True
                )

                # 방금 업로드한 이미지를 변수에 저장
                last_uploaded_image = content
            else:
                # 비회원은 세션을 사용하여 처리
                uploader = Upload(request)
                result = uploader.upload_url(image_url)

                if result:
                    image_id, saved_url = result

                    # 템플릿에서 사용할 가상 객체 생성
                    class NonMemberContent:
                        def __init__(self, id, url):
                            self.id = id
                            self.url_image = type("obj", (object,), {"url": url})
                            self.is_nonmember = True  # 비회원 이미지임을 표시

                    # 가상 객체 생성
                    last_uploaded_image = NonMemberContent(image_id, saved_url)

            # 이미지를 업로드 하면 분석, 삭제 버튼이 생성되도록 함
            is_upload = True

            # 업로드 후 다시 사용한 횟수/남은 횟수 갱신
            nonmember_dict = request.session.get(settings.UPLOAD_SESSION_ID, {})
            used_count = len(nonmember_dict)
            coin = max(0, MAX_NONMEMBER_UPLOADS - used_count)
            limit_exceeded = coin <= 0

        except Exception as e:
            print(f"업로드 중 오류가 발생했습니다: {e}")
            form.add_error("url", f"이미지를 불러오는 중 오류가 발생했습니다.: {e}")

    return render(
        request,
        "upload/upload_page.html",
        {
            "form": form,
            "last_uploaded_image": last_uploaded_image,
            "is_upload": is_upload,
            "coin": coin,
            "limit_exceeded": limit_exceeded,
        },
    )


def initialize(request):

    if request.method == "POST":

        # 세션에서 비회원 업로드 기록(dict) 가져오기
        nonmember_dict = request.session.get(settings.UPLOAD_SESSION_ID, {})

        # 사용한 횟수, 남은 횟수 계산
        used_count = len(nonmember_dict)

        # 게임에서 얻은 추가 코인 반영
        additional_coin = request.session.get('additional_coin', 0)

        coin = max(0, MAX_NONMEMBER_UPLOADS - used_count + additional_coin)
        limit_exceeded = coin <= 0

        # 세션 기록 삭제
        # request.session[settings.UPLOAD_SESSION_ID] = {}
        # request.session.modified = True

        # 초기화 후 남은 횟수는 MAX_NONMEMBER_UPLOADS
        context = {
            "form": URLImageForm(),
            "last_uploaded_image": None,
            "is_upload": False,
            "coin": coin,  # 계산된 실제 남은 횟수 사용
            "limit_exceeded": limit_exceeded,
        }

        html = render_to_string("upload/upload_page.html", context, request=request)
        return JsonResponse({"status": "success", "html": html})

    return JsonResponse({"status": "error"}, status=400)
