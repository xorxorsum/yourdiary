from django.db import models
from django.contrib.auth.models import User

class UserParams(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)  # Пользователь, к которому привязаны настройки
    tasks_solved = models.IntegerField()
    tasks_failed = models.IntegerField()
    score = models.IntegerField()
    avatar = models.ImageField(default='users_avatars/default_avatar.png',upload_to='users_avatars/')


class Tasks(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)  # Пользователь, к которому привязаны таски
    hostId = models.DateField()
    title = models.CharField(max_length=50)
    comment = models.TextField(max_length=5000)
    deadline = models.DateField()
    icon = models.CharField(max_length=20, default='fa-question')
    color = models.CharField(max_length=20, default='#000000')
    done_indicator = models.IntegerField(default=-1)


