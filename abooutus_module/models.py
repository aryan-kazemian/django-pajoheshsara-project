from django.db import models

# Create your models here.

class AboutUsModel(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام تنظیمات')
    main_text = models.TextField(verbose_name='متن اصلی ')
    second_text = models.TextField(verbose_name='متن دوم')
    address = models.CharField(max_length=200, verbose_name='ادرس')
    phone_number = models.CharField(max_length=20, verbose_name='تلفن')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'درباره ی ما'
        verbose_name_plural = 'درباره ی ما'

    def __str__(self):
        return self.name

