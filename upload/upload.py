from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from urllib import request as urllib_request
from datetime import datetime
import os
import uuid


class Upload:
    def __init__(self, request):
        self.session = request.session
        nonmember_url = self.session.get(settings.UPLOAD_SESSION_ID)

        if not nonmember_url:
            nonmember_url = self.session[settings.UPLOAD_SESSION_ID] = {}

        self.nonmember_url = nonmember_url

    def upload_url(self, url):
        """
        비회원이 이미지 URL을 업로드 하는 메서드
        """
        try:
            # URL에서 이미지 다운로드
            image_url = url
            image_name = image_url.split("/")[-1]  # URL에서 파일명 추출

            # URL에서 이미지 가져오기
            response = urllib_request.urlopen(image_url)
            image_data = response.read()

            # 유니크한 파일명 생성
            unique_filename = f"{uuid.uuid4().hex}.jpg"
            temp_dir = os.path.join("upload", "nonmember")
            temp_path = os.path.join(temp_dir, unique_filename)

            # 디렉토리가 없으면 생성
            full_path = os.path.join(settings.MEDIA_ROOT, temp_dir)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                print(f"디렉토리 생성됨: {full_path}")

            # 이미지를 임시 위치에 저장
            saved_path = default_storage.save(
                temp_path, ContentFile(image_data, name=unique_filename)
            )
            image_url = default_storage.url(saved_path)

            # 세션에 이미지 정보 저장
            image_id = str(uuid.uuid4().hex)
            self.nonmember_url[image_id] = {
                "original_url": url,
                "saved_path": saved_path,
                "image_url": image_url,
                "name": image_name,
                "created_at": str(datetime.now()),
            }

            self.save()
            print(f"이미지 업로드 성공 - ID: {image_id}, URL: {image_url}")
            return (image_id, image_url)
        except Exception as e:
            print(f"이미지 업로드에 문제가 발생: {e}")
            import traceback

            traceback.print_exc()
            return None

    def get_image_url(self, image_id):
        """
        세션에서 이미지 URL을 가져오는 메서드
        """
        if image_id in self.nonmember_url:
            return self.nonmember_url[image_id]["image_url"]

        return None

    def save(self):
        """
        세션에 비회원이 업로드한 이미지 url을 저장
        """
        self.session[settings.UPLOAD_SESSION_ID] = self.nonmember_url
        self.session.modified = True
