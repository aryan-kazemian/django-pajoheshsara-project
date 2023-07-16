from django.db import models

# Create your models here.

class ScienceSubjectModel(models.Model):
    title = models.CharField(max_length=300, verbose_name='موضوع علمی')
    url_title = models.CharField(max_length=500, unique=True, null=True, verbose_name=' موضوع علمی در url')
    text1 = models.TextField(verbose_name='متن')
    text2 = models.TextField(verbose_name='متن', null=True, blank=True)
    text3 = models.TextField(verbose_name='متن', null=True, blank=True)
    text4 = models.TextField(verbose_name='متن', null=True, blank=True)
    text5 = models.TextField(verbose_name='متن', null=True, blank=True)
    text6 = models.TextField(verbose_name='متن', null=True, blank=True)
    text7 = models.TextField(verbose_name='متن', null=True, blank=True)
    text8 = models.TextField(verbose_name='متن', null=True, blank=True)
    image_on_science_list_page = models.ImageField(upload_to='science', verbose_name="تصویر در لیست موضوعات علمی")
    image_on_science_detail_page = models.ImageField(upload_to='science', verbose_name="تصویر در جزییات موضوع علمی")
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'موضوع علمی'
        verbose_name_plural = 'موضوعات علمی'
