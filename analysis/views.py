import os
import sys
import shutil
import subprocess
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from upload.models import Content
from upload.upload import Upload
from .models import Analysis
from collections import Counter

def analyze_image(request, image_id=None):
    """
    이미지 분석 함수 (회원 및 비회원 모두 지원)
    """
    result = None

    if request.method == "POST" and 'image_id' in request.POST:
        image_id = request.POST['image_id']

    if request.user.is_authenticated and not image_id:
        # 로그인한 사용자의 마지막 업로드 이미지 분석
        try:
            content = Content.objects.filter(user=request.user).latest('create_at')
            image_path = content.url_image.path
            image_name = os.path.basename(content.url_image.name)
            image_url = content.url_image.url
        except Content.DoesNotExist:
            return JsonResponse({"error": "분석할 이미지가 없습니다."})
    
    elif image_id:
        # 비회원 이미지 분석
        uploader = Upload(request)
        image_url = uploader.get_image_url(image_id)

        if not image_url:
            return JsonResponse({"error": "이미지를 찾을 수 없습니다."})
        
        # 세션에서 이미지 정보 가져오기
        nonmember_url = request.session.get(settings.UPLOAD_SESSION_ID, {})
        image_info = nonmember_url.get(image_id)

        if not image_info:
            return JsonResponse({"error": "이미지 정보를 찾을 수 없습니다."})
        
        # 이미지 경로 구성
        image_path = os.path.join(settings.MEDIA_ROOT, image_info['saved_path'])
        original_name = os.path.basename(image_path)

        # 파일명에서 쿼리 파라미터 제거
        if '?' in original_name:
            original_name = original_name.split('?')[0]

        # 허용되지 않는 문자 제거
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '&', '=']
        image_name = ''.join(c for c in original_name if c not in invalid_chars)

        # 이름이 너무 길면 잘라내기
        if len(image_name) > 50:
            image_name = image_name[:50]

        image_url = image_info['image_url']
    
    else:
        return JsonResponse({"error": "분석할 이미지 정보가 없습니다."})
    
    try:
        # 이미지를 ml_models/samples 디렉터리에 복사
        samples_dir = os.path.join(settings.BASE_DIR, 'analysis', 'ml_models', 'samples')
        os.makedirs(samples_dir, exist_ok=True)
        sample_path = os.path.join(samples_dir, image_name)

        # 동일 이름의 파일이 있으면 제거
        if os.path.exists(sample_path):
            os.remove(sample_path)
        
        # 이미지 복사
        shutil.copy2(image_path, sample_path)

        # font_detection.py 스크립트 실행
        script_path = os.path.join(settings.BASE_DIR, 'analysis', 'ml_models', 'font_detection.py')
        samples_dir = os.path.join(settings.BASE_DIR, 'analysis', 'ml_models', 'samples')
        result_dir = os.path.join(settings.BASE_DIR, 'analysis', 'ml_models', 'result')

        # 파일 확장자 제거
        image_base_name = os.path.splitext(image_name)[0]

        # 폰트 감지 명령어 실행
        image_name = os.path.basename(sample_path)
        process = subprocess.run([sys.executable, script_path],
                       cwd=os.path.join(settings.BASE_DIR, 'analysis', 'ml_models'),
                       capture_output=True, text=True)
        
        # 스크립트 에러 코드
        print(f"스크립트 경로: {script_path}")
        print(f"작업 디렉토리: {os.path.join(settings.BASE_DIR, 'analysis', 'ml_models')}")
        print(f"프로세스 반환 코드: {process.returncode}")
        print(f"표준 출력: {process.stdout}")
        print(f"오류 출력: {process.stderr}")

        if process.returncode != 0:
            return JsonResponse({"error": f"폰트 분석 스크립트 실행 실패: {process.stderr}"})
        
        # 결과 파일 읽기
        result_dir = os.path.join(settings.BASE_DIR, 'analysis', 'ml_models', 'result')
        result_file = os.path.join(result_dir, f'res_{image_base_name}.txt')

        if not os.path.exists(result_file):
            return JsonResponse({"error": "폰트 분석 결과 파일을 찾을 수 없습니다."})

        # 결과 파일에서 폰트 정보 추출
        fonts = []
        with open(result_file, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 9:  # 좌표와 폰트 이름이 있는지 확인
                    font_name = parts[8].strip()
                    if font_name:
                        fonts.append(font_name)

        # 폰트 빈도 집계
        font_counter = Counter(fonts)
        most_common_fonts = font_counter.most_common()

        if not most_common_fonts:
            return JsonResponse({"error": "이미지에서 폰트를 감지할 수 없습니다."})
        
        # 응답 데이터 생성
        primary_font = most_common_fonts[0][0]

        # 폰트 정보 문자열 생성
        if len(most_common_fonts) > 1:
            other_fonts = [f"{font[0]} ({font[1]}회)" for font in most_common_fonts[1:3]]
            font_info = f"주요 폰트: {primary_font} ({most_common_fonts[0][1]}회). 추가 감지: {', '.join(other_fonts)}"
        else:
            font_info = f"주요 폰트: {primary_font} ({most_common_fonts[0][1]}회)"

         # 데이터베이스에 저장
        analysis = Analysis()
        if request.user.is_authenticated and not image_id:
            analysis.content = content
        else:
            analysis.session_id = request.session.session_key
            analysis.image_id = image_id
        
        analysis.font_name = primary_font
        analysis.font_info = font_info
        analysis.save()

        # 분석된 이미지 URL 생성
        # 1. 이미지 파일 복사
        image_base_name = os.path.splitext(os.path.basename(image_name))[0]
        result_file_path = os.path.join(settings.BASE_DIR, 'analysis', 'ml_models', 'result', f'res_{image_base_name}.jpg')
        media_result_dir = os.path.join(settings.MEDIA_ROOT, 'analysis_results')
        os.makedirs(media_result_dir, exist_ok=True)
        media_result_path = os.path.join(media_result_dir, f'res_{image_base_name}.jpg')

        # 결과 파일이 존재하면 MEDIA_ROOT 내부로 복사
        if os.path.exists(result_file_path):
            shutil.copy2(result_file_path, media_result_path)
            result_image_url = f"{settings.MEDIA_URL}analysis_results/res_{image_base_name}.jpg"
        else:
            result_image_url = image_url  # 결과 이미지가 없으면 원본 유지

        # JSON 응답 준비
        result = {
            "success": True,
            "font_name": primary_font,
            "font_info": font_info,
            "all_fonts": {font: count for font, count in most_common_fonts},
            "image_url": image_url,
            "analyzed_image_url": result_image_url
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        result = {"error": f"분석 중 오류가 발생했습니다: {str(e)}"}

    
    # AJAX 요청인 경우 JSON 응답
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(result)
    
    # 일반 요청인 경우 템플릿 렌더링
    return render(request, 'upload/analysis_result.html', {'result': result})