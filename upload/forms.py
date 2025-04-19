from django import forms
from .models import Content


class URLImageForm(forms.ModelForm):
    url = forms.URLField(label="이미지")

    class Meta:
        model = Content
        fields = []  # url은 직접 처리할 것이므로 model 필드는 비워둔다.
