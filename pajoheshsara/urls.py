"""
URL configuration for pajoheshsara project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-panel/', include('admin_panel.urls')),
    path('admin', admin.site.urls, name='admin'),
    path('', include('home_module.urls')),
    path('account/', include('user_module.urls')),
    path('cantactus/', include('contactus_module.urls')),
    path('aboutus/', include('abooutus_module.urls')),
    path('association/', include('association.urls')),
    path('courses/', include('course_module.urls')),
    path('teachers/', include('teachers_module.urls')),
    path('newes/', include('news_module.urls')),
    path('profile/', include('profile_module.urls')),
    path('dargah-pardakht/', include('zarinpall_module.urls')),
    path('scientific-subject/', include('scientific_subject_module.urls')),
    path('create-xlsx-file/', include('createxlsxfile.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
