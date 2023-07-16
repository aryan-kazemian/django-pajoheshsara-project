from django.contrib import admin
from .models import SiteSettingModel, FooterBoxSubModel, FooterBoxCategoryModel
# Register your models here.

admin.site.register(SiteSettingModel)
admin.site.register(FooterBoxSubModel)
admin.site.register(FooterBoxCategoryModel)
