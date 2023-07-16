from django.db import models
from user_module.models import User
from course_module.models import CoursesModel

# Create your models here.

class TypeChoices(models.TextChoices):
    contact = ("contact", "contact")
    change_course = ("change_course", "change_course")
    new_course = ("new_course", "new_course")
    delete_course = ("delete_course", "delete_course")
    change_prerequisite = ("change_prerequisite", "change_prerequisite")
    new_prerequisite = ("new_prerequisite", "new_prerequisite")
    delete_prerequisite = ("delete_prerequisite", "delete_prerequisite")
    change_course_category = ("change_course_category", "change_course_category")
    new_course_category = ("new_course_category", "new_course_category")
    delete_course_category = ("delete_course_category", "delete_course_category")
    new_association = ("new_association", "new_association")
    change_association = ("change_association", "change_association")
    delete_association = ("delete_association", "delete_association")
    new_association_goal = ('new_association_goal', 'new_association_goal')
    change_association_goal = ('change_association_goal', 'change_association_goal')
    delete_association_goal = ('delete_association_goal', 'delete_association_goal')
    new_association_category = ('new_association_category', 'new_association_category')
    change_association_category = ('change_association_category', 'change_association_category')
    delete_association_category = ('delete_association_category', 'delete_association_category')
    new_science = ('new_science', 'new_science')
    change_science = ('change_science', 'change_science')
    delete_science = ('delete_science', 'delete_science')
    new_news = ('new_news', 'new_news')
    change_news = ('change_news', 'change_news')
    delete_news = ('delete_news', 'delete_news')
    new_user = ('new_user', 'new_user')
    change_user = ('change_user', 'change_user')
    change_main_setting = ('change_main_setting', 'change_main_setting')
    delete_main_setting = ('delete_main_setting', 'delete_main_setting')
    new_main_setting = ('new_main_setting', 'new_main_setting')
    change_about_us = ('change_about_us', 'change_about_us')
    delete_about_us = ('delete_about_us', 'delete_about_us')
    new_about_us = ('new_about_us', 'new_about_us')
    change_footer_category = ('change_footer_category', 'change_footer_category')
    delete_footer_category = ('delete_footer_category', 'delete_footer_category')
    new_footer_category = ('new_footer_category', 'new_footer_category')
    change_footer_sub_category = ('change_footer_sub_category', 'change_footer_sub_category')
    delete_footer_sub_category = ('delete_footer_sub_category', 'delete_footer_sub_category')
    new_footer_sub_category = ('new_footer_sub_category', 'new_footer_sub_category')


class AdminPanelLogModel(models.Model):
    user = models.CharField(max_length=300, null=True)
    thing = models.CharField(max_length=400, null=True)
    date = models.DateField(auto_now=True, null=True, unique=False)
    time = models.TimeField(auto_now=True, null=True, unique=False)
    type = models.CharField(max_length=400, choices=TypeChoices.choices, unique=False)

    def __str__(self):
        return self.type


class AdminPanelShowCoursesDetails(models.Model):
    course = models.ForeignKey(to=CoursesModel, on_delete=models.CASCADE)
    member_counts = models.IntegerField()
    members = models.ManyToManyField(to=User, null=True)

    def __str__(self):
        return self.course.name