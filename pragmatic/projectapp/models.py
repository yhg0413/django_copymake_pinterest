from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    title = models.CharField('제목',max_length=20, null=False)
    des = models.CharField('설명',max_length=150, null=True)
    image = models.ImageField('배너이미지', upload_to='project/banner/', null=False)

    created_at = models.DateTimeField(auto_now=True)