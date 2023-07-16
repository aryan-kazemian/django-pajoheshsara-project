from django import forms
from user_module.models import User
from course_module.models import CoursesCategory, CoursesModel, PrerequisiteModels
from association.models import AssociationModel, AssociationGoals, AssociationsCategories
from scientific_subject_module.models import ScienceSubjectModel
from news_module.models import NewsModel
from sitesetting_module.models import SiteSettingModel, FooterBoxCategoryModel, FooterBoxSubModel
from abooutus_module.models import AboutUsModel

teacher_choices = []
teachers = User.objects.filter(groups=1).all()
for teacher in teachers:
    teacher_choices.append(
        (teacher.username, teacher.username)
    )

category_choices = []
categories = CoursesCategory.objects.filter(is_active=True).all()
for cat in categories:
    category_choices.append(
        (cat.category, cat.category)
    )

course_choices = []
courses = CoursesModel.objects.all()
for course in courses:
    course_choices.append(course.name)

association_category_choices = []
for cat in AssociationsCategories.objects.all():
    association_category_choices.append(cat.category_name)

association_organizer_choices = []
for user in User.objects.all():
    association_organizer_choices.append(user.username)

association_choices = []
for assoc in AssociationModel.objects.all():
    association_choices.append(assoc.association_name)


decoration_choices = ['white_or_dark', 'dark', 'white']

footer_category_choices = []
for cat in FooterBoxCategoryModel.objects.all():
    footer_category_choices.append(cat.category_name)

class AnswerContactForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))


class SearchBoxForm(forms.Form):
    search_box = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "جست و جو",
        'class': 'au-input--w300 au-input--style2',
    }))


class UpdateCoursesForm(forms.ModelForm):

    class Meta:
        model = CoursesModel
        fields = ['name', 'teacher', 'category', 'price', 'situation', 'short_information', 'full_information', 'time',
                  'is_active', 'image_on_course_detail', 'image_on_courses_list', 'register_time']
        widgets = {
            'name': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'teacher': forms.Select(attrs={
                                    'class': 'form-control',
                                            }, choices=teacher_choices),
            'category': forms.Select(attrs={
                                    'class': 'form-control',
                                            }, choices=category_choices),
            'price': forms.NumberInput(attrs={
                                     'class': 'form-control',
                                           }),
            'situation': forms.TextInput(attrs={
                                            'class': 'form-control',
                                                    }),
            'short_information': forms.Textarea(attrs={
                                                'class': 'form-control',
                                                      }),
            'full_information': forms.Textarea(attrs={
                                            'class': 'form-control',
                                                    }),
            'image_on_courses_list': forms.ClearableFileInput(attrs={
                                                'class': 'form-control',
                                                            }),
            'image_on_course_detail': forms.ClearableFileInput(attrs={
                                            'class': 'form-control',
                                                            }),
            'time': forms.TextInput(attrs={
                    'class': 'form-control',
                                            }),
            'is_active': forms.CheckboxInput(attrs={
                                    'class': 'form-control',
                                                    }),
            'register_time': forms.CheckboxInput(attrs={
                'class': 'form-control',
            })
                    }


class UpdatePrerequisiteCourseForm(forms.ModelForm):
    class Meta:
        model = PrerequisiteModels
        fields = ['prerequisite', 'course']
        widgets = {
            'prerequisite': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'course': forms.Select(attrs={
                                    'class': 'form-control',
                                            }, choices=course_choices),
        }


class UpdateCategoryCourseForm(forms.ModelForm):
    class Meta:
        model = CoursesCategory
        fields = ['category', 'category_url', 'is_active']
        widgets = {
            'category': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'category_url': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control'
            })
        }


class UpdateAssociationForm(forms.ModelForm):

    class Meta:
        model = AssociationModel
        fields = ['association_name', 'association_category', 'association_organizer', 'association_time',
                  'association_image', 'association_image_for_detail_page', 'association_short_information',
                  'association_full_information', 'instagram_link', 'twitter_link', 'facebook_link', 'situation',
                  'show_on_main_page', 'is_active']
        widgets = {
            'association_name': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'association_category': forms.Select(attrs={
                                    'class': 'form-control',
                                            }, choices=category_choices),
            'association_organizer': forms.Select(attrs={
                                    'class': 'form-control',
                                            }, choices=association_organizer_choices),
            'association_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'association_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'association_image_for_detail_page': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'association_short_information': forms.Textarea(attrs={
                                                'class': 'form-control',
                                                        }),

            'association_full_information': forms.Textarea(attrs={
                                            'class': 'form-control',
                                                    }),
            'instagram_link': forms.TextInput(attrs={
                    'class': 'form-control',
                                            }),
            'twitter_link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'facebook_link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'situation': forms.TextInput(attrs={
                'class': 'form-control'
                                                }),
            'show_on_main_page': forms.CheckboxInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control'
            })
                    }


class UpdateAssociationGoalsForm(forms.ModelForm):

    class Meta:
        model = AssociationGoals
        fields = ['association', 'is_active', 'goal']
        widgets = {
            'goal': forms.Textarea(attrs={
                                            'class': 'form-control',
                                            }),
            'association': forms.Select(attrs={
                                    'class': 'form-control',
                                            }, choices=association_choices),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control'
            })
                    }


class UpdateAssociationCategoriesForm(forms.ModelForm):

    class Meta:
        model = AssociationsCategories
        fields = ['category_name', 'category_url']
        widgets = {
            'category_name': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'category_url': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
                    }


class UpdateScienceForm(forms.ModelForm):

    class Meta:
        model = ScienceSubjectModel
        fields = ['title', 'url_title', 'image_on_science_detail_page', 'image_on_science_list_page', 'text1', 'text2',
                  'text3', 'text4', 'text5', 'text6', 'text7', 'text8', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'url_title': forms.TextInput(attrs={
                                    'class': 'form-control',
                                            }),
            'text1': forms.Textarea(attrs={
                                            'class': 'form-control',
                                                    }),
            'text2': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text3': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text4': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text5': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text6': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text7': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text8': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'image_on_science_list_page': forms.ClearableFileInput(attrs={
                                                'class': 'form-control',
                                                            }),
            'image_on_science_detail_page': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                                    'class': 'form-control',
                                                    })
                    }


class UpdateNewsForm(forms.ModelForm):

    class Meta:
        model = NewsModel
        fields = ['title', 'url_title', 'date', 'image_on_news_list_page', 'image_on_news_detail_page', 'text1',
                  'text2', 'text3', 'text4', 'text5', 'text6', 'text7', 'text8', 'show_on_index_page', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'url_title': forms.TextInput(attrs={
                                    'class': 'form-control',
                                            }),
            'text1': forms.Textarea(attrs={
                                            'class': 'form-control',
                                                    }),
            'text2': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text3': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text4': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text5': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text6': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text7': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'text8': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'image_on_news_detail_page': forms.ClearableFileInput(attrs={
                                                'class': 'form-control',
                                                            }),
            'image_on_news_list_page': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                                    'class': 'form-control',
                                                    }),
            'show_on_index_page': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'date': forms.Textarea(attrs={
                'class': 'form-control',
            }),

                    }


class UpdateMainSettingForm(forms.ModelForm):

    class Meta:
        model = SiteSettingModel
        fields = ['site_setting_name', 'site_logo_1', 'site_logo_2', 'h1_text_main_page', 'under_h1_text', 'any_button',
                  'button_text', 'button_link', 'decoration', 'footer_text', 'instagram_link', 'twitter_link',
                  'facebook_link', 'footer_phone_number', 'is_active']
        widgets = {
            'site_setting_name': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'h1_text_main_page': forms.TextInput(attrs={
                                    'class': 'form-control',
                                            }),
            'under_h1_text': forms.TextInput(attrs={
                                            'class': 'form-control',
                                                    }),
            'button_text': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'button_link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'instagram_link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'twitter_link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'facebook_link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'footer_phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'footer_text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'site_logo_1': forms.ClearableFileInput(attrs={
                                                'class': 'form-control',
                                                            }),
            'site_logo_2': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                                    'class': 'form-control',
                                                    }),
            'decoration': forms.Select(attrs={
                                    'class': 'form-control',
                                            }, choices=decoration_choices),
            'any_button': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),

                    }


class UpdateAboutUsForm(forms.ModelForm):

    class Meta:
        model = AboutUsModel
        fields = ['name', 'address', 'phone_number', 'main_text', 'second_text', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'main_text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'second_text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),

                    }


class UpdateFooterCategoryForm(forms.ModelForm):

    class Meta:
        model = FooterBoxCategoryModel
        fields = ['url', 'category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
            }),

                    }


class UpdateFooterSubCategoryForm(forms.ModelForm):

    class Meta:
        model = FooterBoxSubModel
        fields = ['category', 'title', 'link']
        widgets = {
            'title': forms.TextInput(attrs={
                                            'class': 'form-control',
                                            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }, choices=footer_category_choices)}
