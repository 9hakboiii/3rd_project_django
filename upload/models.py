from django.db import models


# Create your models here.
class Content(models.Model):

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    url_image = models.ImageField(upload_to="upload/url")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
