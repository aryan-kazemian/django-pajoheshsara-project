from django.contrib import admin

# Register your models here.

from .models import XlsxFiles, TempLink

admin.site.register(TempLink)
admin.site.register(XlsxFiles)