from django.db import models
from user_module.models import User
# Create your models here.


class AssociationsCategories(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="دسته بندی")
    category_url = models.CharField(max_length=100, verbose_name="دسته بندی در url", unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class AssociationModel(models.Model):
    association_name = models.CharField(max_length=60, verbose_name='نام انجمن')
    association_category = models.ForeignKey(to=AssociationsCategories, on_delete=models.CASCADE,
                                             verbose_name='دسته بندی انجمن')
    association_short_information = models.TextField(verbose_name='توضیحات کوتاه انجمن')
    association_organizer = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='برگزار کننده ی انجمن')
    association_image_for_detail_page = models.ImageField(upload_to='associations',
                                                          verbose_name='تصویر در صفحه ی جزییات')
    association_image = models.ImageField(upload_to='associations', verbose_name='تصویر در صفحه ی لیست انجمن ها')
    members_count = models.IntegerField(verbose_name='تعداد اعضای انجمن', null=True, default=0)
    association_time = models.CharField(max_length=200, verbose_name='زمان برگزاری انجمن')
    association_full_information = models.TextField(verbose_name='توضیحات کامل انجمن')
    situation = models.CharField(max_length=200, verbose_name='وضعیت انجمن', null=True)
    twitter_link = models.URLField(verbose_name='لینک توییتر', null=True, blank=True)
    instagram_link = models.URLField(verbose_name='لینک اینستاگرام', null=True, blank=True)
    facebook_link = models.URLField(verbose_name='لینک فیسبوک', null=True, blank=True)
    show_on_main_page = models.BooleanField(default=False, verbose_name='نشان دادن در صفحه ی اصلی')
    is_active = models.BooleanField(verbose_name='فعال / غبر فعال')

    def __str__(self):
        return self.association_name

    class Meta:
        verbose_name = 'انجمن'
        verbose_name_plural = 'انجمن ها'


class AssociationGoals(models.Model):
    goal = models.CharField(verbose_name='هدف', max_length=300, null=True)
    association = models.ForeignKey(to=AssociationModel, on_delete=models.CASCADE, verbose_name='انجمن', null=True)
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', default=True)

    def __str__(self):
        return self.goal

    class Meta:
        verbose_name = 'هدف انجمن'
        verbose_name_plural = 'اهداف انجمن'

