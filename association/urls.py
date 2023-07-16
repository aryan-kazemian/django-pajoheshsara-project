from django.urls import path
from . import views
urlpatterns = [
    path('<page>', views.AssociationView.as_view(), name='all-associations-page'),
    path('cat/<str:category>/<page>', views.AssociationFilter.as_view(), name='association-list-filtered'),
    path('association-detail/<association>', views.association_detail, name='association-detail-page'),
]
