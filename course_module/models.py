from django.db import models
from user_module.models import User
# Create your models here.


class CoursesCategory(models.Model):
    category = models.CharField(max_length=200, verbose_name="دسته بندی دوره")
    category_url = models.CharField(max_length=500, verbose_name='دسته بندی در url')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'دسته بندی دوره'
        verbose_name_plural = 'دسته بندی های دوره'


class CoursesModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام دوره', unique=True)
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='دبیر دوره')
    category = models.ForeignKey(to=CoursesCategory, on_delete=models.CASCADE, verbose_name='دسته بندی دوره')
    price = models.CharField(max_length=200, verbose_name='قیمت دوره')
    situation = models.CharField(max_length=200, verbose_name='وضعیت')
    image_on_courses_list = models.ImageField(upload_to='courses', verbose_name='تصویر دوره در صفحه ی دوره ها')
    image_on_course_detail = models.ImageField(upload_to='courses', verbose_name='تصویر دوره در صفحه ی جزییات دوره')
    short_information = models.TextField(verbose_name='توضیحات کوتاه')
    full_information = models.TextField(verbose_name='توضیحات کامل')
    time = models.CharField(max_length=200, verbose_name='زمان دوره')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')
    register_time = models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'


class PrerequisiteModels(models.Model):
    prerequisite = models.CharField(max_length=500, verbose_name='پیش نیاز')
    course = models.ForeignKey(to=CoursesModel, verbose_name='دوره', on_delete=models.CASCADE)

    def __str__(self):
        return self.prerequisite

    class Meta:
        verbose_name = 'پیش نیاز'
        verbose_name_plural = 'پیش نیاز ها'


class OwnedCoursesUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='کاربر', unique=True)
    courses = models.ManyToManyField(to=CoursesModel, verbose_name='دوره ها', null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'دوره ی خریداری شده'
        verbose_name_plural = 'دوره های خریداری شده'


class ProfitCourseModel(models.Model):
    price = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    user = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.price
