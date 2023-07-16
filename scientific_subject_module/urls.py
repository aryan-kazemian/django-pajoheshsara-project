from django.urls import path
from . import views
urlpatterns = [
    path('<page>', views.science_list, name='science-list-page'),
    path('sciencific-subjects/<science_url>', views.science_detail, name='science-detail-page')
]

