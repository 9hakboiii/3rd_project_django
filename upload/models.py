from django.db import models


# Create your models here.
class Content(models.Model):

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    url_image = models.ImageField(upload_to="upload/url", max_length=500)
    font_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    font_info = models.CharField(max_length=2000, blank=True, null=True, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
