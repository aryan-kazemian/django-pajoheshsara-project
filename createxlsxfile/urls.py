from django.urls import path
from . import views

urlpatterns = [
    path('<id>', views.create_xlsx_file, name='create-xlsx-file'),
    path('file/<id>', views.before_download_file, name='before_download-file'),
    path('download-file/<uuid:link>', views.download_file, name='download-file')
]
