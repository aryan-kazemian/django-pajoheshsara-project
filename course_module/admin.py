from django.contrib import admin
from .models import CoursesModel, CoursesCategory, PrerequisiteModels, OwnedCoursesUser, ProfitCourseModel

admin.site.register(CoursesCategory)
admin.site.register(CoursesModel)
admin.site.register(PrerequisiteModels)
admin.site.register(OwnedCoursesUser)
admin.site.register(ProfitCourseModel)
