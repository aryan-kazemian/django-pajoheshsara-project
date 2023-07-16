from django.db import models
from user_module.models import User

# Create your models here.

class SenderChoices(models.TextChoices):
    teacher = "teacher", "دبیر"
    user = "user", "کابر"

class ChatModel(models.Model):
    teacher = models.CharField(max_length=200, verbose_name='نام کاربری دبیر')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    sender = models.CharField(max_length=200, verbose_name='فرستنده', choices=SenderChoices.choices)
    text = models.TextField(verbose_name='متن')
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ', null=True)
    time = models.TimeField(auto_now_add=True, verbose_name='زمان', null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'چت'
        verbose_name_plural = "چت ها"
