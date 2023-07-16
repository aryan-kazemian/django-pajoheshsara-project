from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class GradeChoices(models.TextChoices):
    Preschool = ("پیش دبستانی", "پیش دبستانی")
    first_grade = ("اول", "اول")
    second_grade = ("دوم", "دوم")
    third_grade = ("سوم", "سوم")
    fourth_grade = ("چهارم", "چهارم")
    fifth_grade = ("پنجم", "پنجم")
    sixth_grade = ("ششم", "ششم")
    seventh_grade = ("هفتم", "هفتم")
    eighth_grade = ("هشتم", "هشتم")
    ninth_grade = ("نهم", "نهم")
    tenth_grade = ("دهم", "دهم")
    eleventh_grade = ("یازدهم", "یازدهم")
    twelfth_grade = ("دوازدهم", "دوازدهم")


class User(AbstractUser):
    user_random_cod = models.CharField(max_length=500, verbose_name='کد امنیتی اکانت')
    user_random_string = models.CharField(max_length=500, verbose_name='رشته ی امنیتی اکانت', null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars', verbose_name='آواتار', blank=True, null=True)
    about_user = models.TextField(blank=True, null=False, verbose_name='درباره ی اکانت')
    phone_number = models.CharField(max_length=12, verbose_name='شماره موبایل')
    father_name = models.CharField(max_length=100, verbose_name='نام پدر', null=True, blank=True)
    kode_meli = models.CharField(max_length=30, verbose_name='کد ملی', null=True, blank=True)
    background_image = models.ImageField(upload_to='background-images-user', null=True, verbose_name='تصویر پس زمینه', blank=True)
    missed_cod = models.IntegerField(default=0, editable=False)
    missed_cod_time = models.CharField(null=True, editable=False, max_length=100)
    grade = models.CharField(null=True, max_length=100, choices=GradeChoices.choices)
    school = models.CharField(max_length=200, null=True)
    home_phone_number = models.CharField(max_length=12, null=True)
    birthday = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'



