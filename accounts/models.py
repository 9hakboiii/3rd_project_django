from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = "M", "남자"
        FEMALE = "F", "여자"

    gender = models.CharField(
        verbose_name="성별", max_length=1, choices=GenderChoices.choices
    )

    JOBS = (
        ("P", "교수/강사(Professor/Lecturer)"),
        ("S", "학생(Student)"),
        ("R", "연구원(Researcher)"),
        ("E", "기타(Etc.)"),
    )

    job = models.CharField(verbose_name="직업", max_length=1, choices=JOBS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
