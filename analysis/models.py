from django.db import models
from upload.models import Content

class Analysis(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True) 
    font_name = models.CharField(max_length=100)
    font_info = models.CharField(max_length=500)
    analysis_data = models.DateTimeField(auto_now_add=True)

    # 비회원 분석을 위한 세션 정보 저장
    session_id = models.CharField(max_length=100, null=True, blank=True)
    image_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.content:
            return f"{self.content.user}의 이미지 분석: {self.font_name}"
        return f"비회원 이미지 분석: {self.font_name}"
    
