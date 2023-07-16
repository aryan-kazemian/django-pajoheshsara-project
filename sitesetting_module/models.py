from django.db import models

# Create your models here.

class DropDownChoicesDecoration(models.TextChoices):
    white = "white", "روشن"
    dark = "dark", "تیره"
    white_or_dark = "white_or_dark", "انتخواب کاربر"


class SiteSettingModel(models.Model):
    site_setting_name = models.CharField(max_length=50, verbose_name='نام تنظیمات')
    site_logo_1 = models.ImageField(upload_to='site-logo', verbose_name='لوگو ی سایت')
    site_logo_2 = models.ImageField(upload_to='site-logo', verbose_name='لوگو ی سایت', null=True)
    h1_text_main_page = models.CharField(max_length=70, verbose_name='عنوان سایز h1 در بالا ی صفحه ی اصلی')
    under_h1_text = models.TextField(verbose_name='متن زیر عنوان h1')
    any_button = models.BooleanField(verbose_name='دکمه ی زیر متن فعال / غیر فعال')
    button_text = models.CharField(max_length=30, verbose_name='نوشته ی دکمه', null=True, blank=True)
    button_link = models.URLField(verbose_name='لینک دکمه', null=True, blank=True)
    decoration = models.CharField(choices=DropDownChoicesDecoration.choices, verbose_name='دکوریشن', max_length=100, null=True)
    footer_text = models.TextField(verbose_name='متن فوتر')
    instagram_link = models.URLField(verbose_name='لینک اینستاگرام')
    twitter_link = models.URLField(verbose_name='لینک توییتر')
    facebook_link = models.URLField(verbose_name='لینک فیس بوک')
    footer_phone_number = models.CharField(max_length=15, verbose_name='شماره تماس در فوتر')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', null=True)

    class Meta:
        verbose_name = 'تنظیم سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return self.site_setting_name


class FooterBoxCategoryModel(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='عنوان دسته بندی')
    url = models.CharField(max_length=500, verbose_name='url', null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'دسته یندی فوتر'
        verbose_name_plural = 'دسته بندی ها ی فوتر'


class FooterBoxSubModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    link = models.URLField(max_length=500, verbose_name='لینک')
    category = models.ForeignKey(to=FooterBoxCategoryModel, on_delete=models.CASCADE, verbose_name='دسته بندی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لینک'
        verbose_name_plural = 'لینک های فوتر'
