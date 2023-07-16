from django.db import models

# Create your models here.

class ContactUsModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    text = models.TextField(verbose_name='پیام')
    answer = models.TextField(verbose_name='پاسخ', null=True, blank=True)
    dose_answered = models.BooleanField(default=False, verbose_name='جواب داده شده / نشده')
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما'

    def __str__(self):
        return self.name


