from django.db import models

# Create your models here.

class NewsModel(models.Model):
    title = models.CharField(max_length=300, verbose_name='موضوع خبر')
    url_title = models.CharField(max_length=500, unique=True, verbose_name='موضوع خبر در url')
    text1 = models.TextField(verbose_name='متن خبر')
    text2 = models.TextField(verbose_name='متن خبر', null=True, blank=True)
    text3 = models.TextField(verbose_name='متن خبر', null=True, blank=True)
    text4 = models.TextField(verbose_name='متن خبر', null=True, blank=True)
    text5 = models.TextField(verbose_name='متن خبر', null=True, blank=True)
    text6 = models.TextField(verbose_name='متن خبر', null=True, blank=True)
    text7 = models.TextField(verbose_name='متن خبر', null=True, blank=True)
    text8 = models.TextField(verbose_name='متن خبر', null=True, blank=True)
    date = models.CharField(max_length=100, verbose_name='تاریخ')
    image_on_news_list_page = models.ImageField(upload_to='news', verbose_name="تصویر در لیست خبر ها")
    image_on_news_detail_page = models.ImageField(upload_to='news', verbose_name="تصویر در جزییات خبر")
    show_on_index_page = models.BooleanField(default=False, verbose_name='نشان دادن در صفحه ی اصلی')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'
