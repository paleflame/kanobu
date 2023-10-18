from django.db import models
from datetime import datetime

# Create your models here.


def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    extension = filename.split('.')[-1]
    return f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}.{extension}"

class UploadedImage(models.Model):
    image = models.ImageField(upload_to=directory_path)