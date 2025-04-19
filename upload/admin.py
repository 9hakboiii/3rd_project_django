from django.contrib import admin
from django.utils.html import format_html
from upload.models import Content
import os
from django.conf import settings


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "url_image", "create_at", "update_at"]
    list_filter = ["user", "create_at"]
    search_fields = ["user__username"]
    actions = ["delete_selected_with_files"]

    def display_image(self, obj):
        """Admin 페이지에서 이미지 미리보기 표시"""
        if obj.url_image:
            return format_html('<img src="{}" width="100" />', obj.url_image.url)
        return "이미지 없음"

    display_image.short_description = "이미지 미리보기"

    def delete_model(self, request, obj):
        """단일 객체 삭제 시 이미지 파일도 함께 삭제"""
        # 이미지 파일 경로 저장
        if obj.url_image:
            file_path = obj.url_image.path
            # 데이터베이스에서 객체 삭제
            obj.delete()
            # 파일 시스템에서 이미지 파일 삭제
            if os.path.isfile(file_path):
                os.remove(file_path)
        else:
            obj.delete()

    def delete_queryset(self, request, queryset):
        """여러 객체 일괄 삭제 시 이미지 파일도 함께 삭제"""
        for obj in queryset:
            if obj.url_image:
                file_path = obj.url_image.path
                # 파일 시스템에서 이미지 파일 삭제
                if os.path.isfile(file_path):
                    os.remove(file_path)
        # 데이터베이스에서 queryset 삭제
        queryset.delete()

    @admin.action(description="선택된 항목과 이미지 파일 삭제")
    def delete_selected_with_files(self, request, queryset):
        """사용자 정의 액션: 선택된 항목과 이미지 파일 삭제"""
        self.delete_queryset(request, queryset)
