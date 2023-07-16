from django.contrib import admin
from .models import AssociationModel, AssociationGoals, AssociationsCategories

# Register your models here.

admin.site.register(AssociationGoals)
admin.site.register(AssociationModel)
admin.site.register(AssociationsCategories)

