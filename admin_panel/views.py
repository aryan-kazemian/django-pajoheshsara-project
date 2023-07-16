import datetime
from .models import AdminPanelLogModel, AdminPanelShowCoursesDetails
from django.shortcuts import render, redirect
from django.views import View
from functions.functions import make_grope
from .forms import AnswerContactForm, SearchBoxForm, UpdateCoursesForm, UpdatePrerequisiteCourseForm,\
    UpdateCategoryCourseForm, UpdateAssociationForm, UpdateAssociationGoalsForm, UpdateAssociationCategoriesForm,\
    UpdateScienceForm, UpdateNewsForm, UpdateMainSettingForm, UpdateAboutUsForm, UpdateFooterCategoryForm,\
    UpdateFooterSubCategoryForm
from association.models import AssociationModel, AssociationGoals, AssociationsCategories
from sitesetting_module.models import SiteSettingModel, FooterBoxSubModel, FooterBoxCategoryModel
from contactus_module.models import ContactUsModel
from course_module.models import CoursesModel, PrerequisiteModels, CoursesCategory, ProfitCourseModel, OwnedCoursesUser
from scientific_subject_module.models import ScienceSubjectModel
from news_module.models import NewsModel
from user_module.models import User
from abooutus_module.models import AboutUsModel
import jalali_date
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


paginate_by = 20

@login_required
def admin_index(request):
    user = request.user
    if not user.is_staff:
        return render(request, '404/404.html')
    active_courses_count = CoursesModel.objects.filter(is_active=True).all()
    today_date = datetime.date.today()
    profits_today = ProfitCourseModel.objects.all()
    today_profit = 0
    this_month_profit = 0
    this_year_profit = 0
    this_jalali_month = str(jalali_date.date2jalali(datetime.date.today()))[5:7]
    this_jalali_year = str(jalali_date.date2jalali(datetime.date.today()))[:4]
    for profit in profits_today:
        if profit.date == today_date:
            today_profit += int(profit.price)
        if str(jalali_date.date2jalali(profit.date))[5:7] == this_jalali_month:
            this_month_profit += int(profit.price)
        if str(jalali_date.date2jalali(profit.date))[:4] == this_jalali_year:
            this_year_profit += int(profit.price)
    logs = AdminPanelLogModel.objects.all()[::-1]
    own_courses = OwnedCoursesUser.objects.all()
    active_courses = []
    for course in active_courses_count:
        active_courses.append([course])
    all_users_courses = []
    for own in own_courses:
        user_course_list = [own.user]
        for c in own.courses.all():
            user_course_list.append(c.name)
        all_users_courses.append(user_course_list)
    for index, course in enumerate(active_courses):
        member_count = 0
        members = []
        for list in all_users_courses:
            if course[0].name in list[1:]:
                member_count += 1
                members.append(list[0])
        active_courses[index].append(member_count)
        active_courses[index].append(members)
    for list in active_courses:
        check: bool = AdminPanelShowCoursesDetails.objects.filter(course_id=list[0].id)
        if check:
            model = AdminPanelShowCoursesDetails.objects.filter(course_id=list[0].id).first()
            model.member_counts = list[1]
            model.save()
        else:
            new_show_detail = AdminPanelShowCoursesDetails(
                course_id=list[0].id,
                member_counts=list[1],
                )
            new_show_detail.save()
    courses_details = AdminPanelShowCoursesDetails.objects.all()
    context = {
        'active_courses': active_courses_count.count(),
        'today_profit': today_profit,
        'month_profit': this_month_profit,
        'year_profit': this_year_profit,
        'logs': logs[:30],
        'courses_details': courses_details,
    }
    return render(request, 'admin-panel/admin-index.html', context)

@login_required
def admin_header_render_partial(request):
    user = request.user
    if not user.is_staff :
        return render(request , '404/404.html')
    contacts = ContactUsModel.objects.filter(dose_answered=False).all()
    context = {
        'user': request.user,
        'site_settings': SiteSettingModel.objects.filter(is_active=True).first(),
        'contacts': contacts[::-1],
        'contacts_count': contacts.count()
    }
    return render(request, 'admin-panel/base/includes/header.html', context)

@login_required
def admin_panel_course_users_detail_list(request, id):
    user = request.user
    if not user.is_staff :
        return render(request , '404/404.html')
    main_course = AdminPanelShowCoursesDetails.objects.get(id=id).course
    own_courses = OwnedCoursesUser.objects.all()
    users = []
    for user_courses in own_courses:
        courses = user_courses.courses.all()
        for course in courses:
            if course.id == main_course.id:
                users.append(user_courses.user)
    context = {
            'users': users,
            'pk': id,
    }
    return render(request, 'admin-panel/admin-panel-courses-users-details.html', context)

@method_decorator(login_required, 'dispatch')
class AnswerContactsView(View):
    def get(self, request, id):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        contact = ContactUsModel.objects.filter(id=id).first()
        form = AnswerContactForm
        context = {
            'form': form,
            'contact': contact,
        }
        return render(request, 'admin-panel/contacts.html', context)

    def post(self, request, id):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = AnswerContactForm(request.POST)
        if form.is_valid():
            contact = ContactUsModel.objects.filter(pk=id).first()
            text = form.cleaned_data.get('text')
            contact.answer = text
            contact.dose_answered = True
            contact.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='contact',
                user=str(user.username),
                thing=str(contact.subject)
            )
            new_log.save()
            # todo : to send the message
            return redirect('admin-panel')

        context = {
            'form': form
        }
        return render(request, 'admin-panel/contacts.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCoursesListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            courses = CoursesModel.objects.all()
        else:
            courses = CoursesModel.objects.filter(name__iregex=search).all()
            if courses is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_courses = make_grope(courses, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(courses) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_courses) < len(courses):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(courses)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'courses': all_courses,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/courses.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            courses = CoursesModel.objects.filter(name__iregex=search).all()
            if len(courses) < 1:
                index = int(int(page) - 1)
                all_courses = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(courses) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_courses) < len(courses):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(courses)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'courses': all_courses[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request , 'admin-panel/courses.html' , context)
            else:
                index = int(int(page) - 1)
                all_courses = make_grope(courses, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(courses) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_courses) < len(courses):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(courses)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'courses': all_courses[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/courses.html', context)
        return redirect('admin-panel-courses-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelCourseChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        course = CoursesModel.objects.filter(id=pk).first()
        form = UpdateCoursesForm(initial={
            'name': course.name,
            'teacher': course.teacher,
            'category': course.category,
            'price': course.price,
            'situation': course.situation,
            'image_on_courses_list': course.image_on_courses_list.url,
            'image_on_course_detail': course.image_on_course_detail.url,
            'short_information': course.short_information,
            'full_information': course.full_information,
            'time': course.time,
            'is_active': course.is_active,
            'register_time': course.register_time,
        })
        context = {
            'form': form,
            'pk': pk,
            'course': course
        }
        return render(request, 'admin-panel/change_course_detail.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        course = CoursesModel.objects.filter(id=pk).first()
        edit_form = UpdateCoursesForm(request.POST, request.FILES, instance=course)
        if edit_form.is_valid():
            name = edit_form.cleaned_data.get('name')
            teacher = edit_form.cleaned_data.get('teacher')
            category = edit_form.cleaned_data.get('category')
            price = edit_form.cleaned_data.get('price')
            situation = edit_form.cleaned_data.get('situation')
            short_information = edit_form.cleaned_data.get('short_information')
            full_information = edit_form.cleaned_data.get('full_information')
            is_active = edit_form.cleaned_data.get('is_active')
            image_list = edit_form.cleaned_data.get('image_on_courses_list')
            image_detail = edit_form.cleaned_data.get('image_on_course_detail')
            register_time = edit_form.cleaned_data.get('register_time')
            course.name = name
            course.teacher = teacher
            course.category = category
            course.price = price
            course.situation = situation
            course.short_information = short_information
            course.full_information = full_information
            course.is_active = is_active
            course.image_on_courses_list = image_list
            course.image_on_course_detail = image_detail
            course.register_time = register_time
            course.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_course',
                user=str(user.username),
                thing=str(course.name)
            )
            new_log.save()
            return redirect('admin-panel-change-course', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change_course_detail.html', context),

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewCourse(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateCoursesForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-course.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateCoursesForm(request.POST, request.FILES)
        if form.is_valid():
            new_course = CoursesModel(name=form.cleaned_data.get('name'),
                                      teacher=form.cleaned_data.get('teacher'),
                                      category=form.cleaned_data.get('category'),
                                      price=form.cleaned_data.get('price'),
                                      situation=form.cleaned_data.get('situation'),
                                      image_on_courses_list=form.cleaned_data.get('image_on_courses_list'),
                                      image_on_course_detail=form.cleaned_data.get('image_on_course_detail'),
                                      short_information=form.cleaned_data.get('short_information'),
                                      full_information=form.cleaned_data.get('full_information'),
                                      time=form.cleaned_data.get('time'),
                                      is_active=form.cleaned_data.get('is_active'),
                                      register_time=form.cleaned_data.get('register_time')
                                      )
            new_course.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_course',
                user=str(user.username),
                thing=str(new_course.name)
            )
            new_log.save()
            return redirect('admin-panel-courses-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-course.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteCourse(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        course = CoursesModel.objects.filter(id=pk).first()
        context = {
            'course': course
        }
        return render(request, 'admin-panel/delete_course.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        course = CoursesModel.objects.filter(id=pk).first()
        course.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_course',
            user=str(user.username),
            thing=str(course.name)
        )
        new_log.save()
        return redirect('admin-panel-courses-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelPrerequisiteListView(View):

    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        if search == 'all':
            prerequisites = PrerequisiteModels.objects.all()
        else:
            prerequisites = PrerequisiteModels.objects.filter(course__name__regex=search).all()[::-1]
        index = int(int(page) - 1)
        all_prerequisites = make_grope(prerequisites, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(prerequisites) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_prerequisites) < len(prerequisites):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(prerequisites)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'prerequisites': all_prerequisites,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
        }
        return render(request, 'admin-panel/prerequisite-courses.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            prerequisites = PrerequisiteModels.objects.filter(course__name__iregex=search)
            if len(prerequisites) < 1:
                index = int(int(page) - 1)
                all_prerequisites = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(prerequisites) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_prerequisites) < len(prerequisites):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(prerequisites)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'prerequisites': all_prerequisites[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/prerequisite-courses.html', context)
            else:
                index = int(int(page) - 1)
                all_prerequisites = make_grope(prerequisites, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(prerequisites) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_prerequisites) < len(prerequisites):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(prerequisites)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'prerequisites': all_prerequisites[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/prerequisite-courses.html', context)

        return redirect('admin-panel-prerequisites-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class DeletePrerequisiteView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        prerequisite = PrerequisiteModels.objects.filter(id=pk).first()
        context = {
            'prerequisite': prerequisite
        }
        return render(request, 'admin-panel/delete-prerequisite-course.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        prerequisite = PrerequisiteModels.objects.filter(id=pk).first()
        course = prerequisite.course
        prerequisite.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_prerequisite',
            user=str(user.username),
            thing=str(course.name)
        )
        new_log.save()
        return redirect('admin-panel-prerequisites-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelPrerequisiteChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        prerequisite = PrerequisiteModels.objects.filter(id=pk).first()
        form = UpdatePrerequisiteCourseForm(initial={
                'prerequisite': prerequisite.prerequisite,
                'course': prerequisite.course
        })
        context = {
            'form': form,
            'pk': pk,
            'course': prerequisite
        }
        return render(request, 'admin-panel/prerequisite-change-detail.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        prerequisite = PrerequisiteModels.objects.filter(id=pk).first()
        form = UpdatePrerequisiteCourseForm(request.POST, instance=prerequisite)
        if form.is_valid():
            prerequisite_form = form.cleaned_data.get('prerequisite')
            course = form.cleaned_data.get('course')
            prerequisite.prerequisite = prerequisite_form
            prerequisite.course = course
            prerequisite.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_prerequisite',
                user=str(user.username),
                thing=str(course.name)
            )
            new_log.save()
            return redirect('admin-panel-change-prerequisite-course', pk)

        context = {
            'form': form,
            'pk': pk,
            'course': prerequisite
        }
        return render(request, 'admin-panel/prerequisite-change-detail.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewPrerequisite(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdatePrerequisiteCourseForm
        context = {
            'form': form
        }
        return render(request, 'admin-panel/new-prqrequisite.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdatePrerequisiteCourseForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            prerequisite = form.cleaned_data.get('prerequisite')
            new_prerequisite = PrerequisiteModels(
                prerequisite=prerequisite,
                course=course
            )
            new_prerequisite.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_prerequisite',
                user=str(user.username),
                thing=str(course.name)
            )
            new_log.save()
            return redirect('admin-panel-prerequisites-list', 'all', 1)

        context = {
            'form': form
        }
        return render(request, 'admin-panel/new-prqrequisite.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCategoryCourseListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        if search == 'all':
            categories = CoursesCategory.objects.all()
        else:
            categories = CoursesCategory.objects.filter(category__iregex=search).all()[::-1]
        index = int(int(page) - 1)
        all_categories = make_grope(categories, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(categories) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_categories) < len(categories):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(categories)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'categories': all_categories,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
        }
        return render(request, 'admin-panel/course-categories-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            categories = CoursesCategory.objects.filter(category__iregex=search).all()
            if len(categories) < 1:
                all_categories = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(categories) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_categories) < len(categories):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(categories)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'categories': all_categories[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/course-categories-list.html', context)
            else:
                index = int(int(page) - 1)
                all_categories = make_grope(categories, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(categories) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_categories) < len(categories):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(categories)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'categories': all_categories[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/course-categories-list.html', context)

        return redirect('admin-panel-categories-course-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class DeleteCourseCategoryView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        cat = CoursesCategory.objects.filter(id=pk).first()
        context = {
            'category': cat
        }
        return render(request, 'admin-panel/delete-course-category.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        cat = CoursesCategory.objects.filter(id=pk).first()
        category = cat.category
        cat.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_course_category',
            user=str(user.username),
            thing=str(category)
        )
        new_log.save()
        return redirect('admin-panel-categories-course-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelCourseCategoryChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        category = CoursesCategory.objects.filter(id=pk).first()
        form = UpdateCategoryCourseForm(initial={
                'category_url': category.category_url,
                'category': category.category,
                'is_active': category.is_active
        })
        context = {
            'form': form,
            'pk': pk,
            'category': category
        }
        return render(request, 'admin-panel/course-category-change.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        category = CoursesCategory.objects.filter(id=pk).first()
        form = UpdateCategoryCourseForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data.get('category')
            is_active = form.cleaned_data.get('is_active')
            category_url = form.cleaned_data.get('category_url')
            category.category = category_name
            category.category_url = category_url
            category.is_active = is_active
            category.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_course_category',
                user=str(user.username),
                thing=str(category)
            )
            new_log.save()
            return redirect('admin-panel-change-course-category-course', pk)

        context = {
            'form': form,
            'pk': pk,
            'category': category,
            'formm': form.category
        }
        return render(request, 'admin-panel/course-category-change.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewCourseCategory(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateCategoryCourseForm
        context = {
            'form': form
        }
        return render(request, 'admin-panel/new-course-category.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateCategoryCourseForm(request.POST)
        if form.is_valid():
            new_course_category = CoursesCategory(
                category=form.cleaned_data.get('category'),
                category_url=form.cleaned_data.get('category_url'),
                is_active=form.cleaned_data.get('is_active'),
            )
            new_course_category.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_course_category',
                user=str(user.username),
                thing=str(form.cleaned_data.get('category'))
            )
            new_log.save()
            return redirect('admin-panel-categories-course-list', 'all', 1)

        context = {
            'form': form
        }
        return render(request, 'admin-panel/new-course-category.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelAssociationListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            association = AssociationModel.objects.all()
        else:
            association = AssociationModel.objects.filter(association_name__iregex=search).all()
            if association is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_association = make_grope(association, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(association) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_association) < len(association):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(association)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'associations': all_association,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/associations.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            association = AssociationModel.objects.filter(association_name__iregex=search).all()
            if len(association) < 1:
                index = int(int(page) - 1)
                all_association = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(association) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_association) < len(association):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(association)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'associations': all_association[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/associations.html', context)
            else:
                index = int(int(page) - 1)
                all_association = make_grope(association, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(association) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_association) < len(association):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(association)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'associations': all_association[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/associations.html', context)
        return redirect('admin-panel-association-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelAssociationChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association = AssociationModel.objects.filter(id=pk).first()
        form = UpdateAssociationForm(initial={
            'association_name': association.association_name,
            'association_category': association.association_category,
            'association_short_information': association.association_short_information,
            'association_organizer': association.association_organizer,
            'association_image_for_detail_page': association.association_image_for_detail_page.url,
            'association_image': association.association_image.url,
            'association_time': association.association_time,
            'association_full_information': association.association_full_information,
            'situation': association.situation,
            'twitter_link': association.twitter_link,
            'instagram_link': association.instagram_link,
            'facebook_link': association.facebook_link,
            'show_on_main_page': association.show_on_main_page,
            'is_active': association.is_active,
        })
        context = {
            'form': form,
            'pk': pk,
            'association': association
        }
        return render(request, 'admin-panel/change-association.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association = AssociationModel.objects.filter(id=pk).first()
        edit_form = UpdateAssociationForm(request.POST, request.FILES, instance=association)
        if edit_form.is_valid():
            association_name = edit_form.cleaned_data.get('association_name')
            association_category = edit_form.cleaned_data.get('association_category')
            association_short_information = edit_form.cleaned_data.get('association_short_information')
            association_organizer = edit_form.cleaned_data.get('association_organizer')
            association_image_for_detail_page = edit_form.cleaned_data.get('association_image_for_detail_page')
            association_image = edit_form.cleaned_data.get('association_image')
            association_time = edit_form.cleaned_data.get('association_time')
            association_full_information = edit_form.cleaned_data.get('association_full_information')
            situation = edit_form.cleaned_data.get('situation')
            twitter_link = edit_form.cleaned_data.get('twitter_link')
            instagram_link = edit_form.cleaned_data.get('instagram_link')
            facebook_link = edit_form.cleaned_data.get('facebook_link')
            show_on_main_page = edit_form.cleaned_data.get('show_on_main_page')
            is_active = edit_form.cleaned_data.get('is_active')
            association.association_name = association_name
            association.association_category = association_category
            association.association_short_information = association_short_information
            association.association_organizer = association_organizer
            association.association_image_for_detail_page = association_image_for_detail_page
            association.association_image = association_image
            association.association_time = association_time
            association.association_full_information = association_full_information
            association.situation = situation
            association.twitter_link = twitter_link
            association.instagram_link = instagram_link
            association.facebook_link = facebook_link
            association.show_on_main_page = show_on_main_page
            association.is_active = is_active
            association.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_association',
                user=str(user.username),
                thing=str(association.association_name)
            )
            new_log.save()
            return redirect('admin-panel-change-association', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-association.html', context),

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewAssociation(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAssociationForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-association.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAssociationForm(request.POST, request.FILES)
        if form.is_valid():
            new_association = AssociationModel(association_name=form.cleaned_data.get('association_name'),
                                               association_category=form.cleaned_data.get('association_category'),
                                               association_short_information=form.cleaned_data
                                               .get('association_short_information'),
                                               association_organizer=form.cleaned_data.get('association_organizer'),
                                               association_image_for_detail_page=form.cleaned_data
                                               .get('association_image_for_detail_page'),
                                               association_image=form.cleaned_data.get('association_image'),
                                               association_time=form.cleaned_data.get('association_time'),
                                               association_full_information=form.cleaned_data
                                               .get('association_full_information'),
                                               situation=form.cleaned_data.get('situation'),
                                               twitter_link=form.cleaned_data.get('twitter_link'),
                                               instagram_link=form.cleaned_data.get('instagram_link'),
                                               facebook_link=form.cleaned_data.get('facebook_link'),
                                               show_on_main_page=form.cleaned_data.get('show_on_main_page'),
                                               is_active=form.cleaned_data.get('is_active'),    )
            new_association.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_association',
                user=str(user.username),
                thing=str(new_association.association_name)
            )
            new_log.save()
            return redirect('admin-panel-association-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-association.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteAssociation(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association = AssociationModel.objects.filter(id=pk).first()
        context = {
            'association': association
        }
        return render(request, 'admin-panel/delete-association.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association = AssociationModel.objects.filter(id=pk).first()
        association.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_association',
            user=str(user.username),
            thing=str(association.association_name)
        )
        new_log.save()
        return redirect('admin-panel-association-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelAssociationGoalsListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        search = 'all'
        is_search_none = False
        if search == 'all':
            association_goals = AssociationGoals.objects.all()
        else:
            association_goals = AssociationGoals.objects.\
                filter(association__association_category__category_name__iregex=search).all()
            if association_goals is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_association_goals = make_grope(association_goals, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(association_goals) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_association_goals) < len(association_goals):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(association_goals)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'associations_goals': all_association_goals,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/association-goals-list.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelAssociationGoalsChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association_goal = AssociationGoals.objects.filter(id=pk).first()
        form = UpdateAssociationGoalsForm(initial={
            'goal': association_goal.goal,
            'association': association_goal.association,
            'is_active': association_goal.is_active,
        })
        context = {
            'form': form,
            'pk': pk,
            'association_goal': association_goal
        }
        return render(request, 'admin-panel/change-association-goals.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association_goal = AssociationGoals.objects.filter(id=pk).first()
        edit_form = UpdateAssociationGoalsForm(request.POST, request.FILES, instance=association_goal)
        if edit_form.is_valid():
            association = edit_form.cleaned_data.get('association')
            goal = edit_form.cleaned_data.get('goal')
            is_active = edit_form.cleaned_data.get('is_active')
            association_goal.association = association
            association_goal.goal = goal
            association_goal.is_active = is_active
            association_goal.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_association_goal',
                user=str(user.username),
                thing=str(association_goal.association.association_name)
            )
            new_log.save()
            return redirect('admin-panel-change-association-goals', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-association-goals.html', context),

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewAssociationGoals(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAssociationGoalsForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-association-goal.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAssociationGoalsForm(request.POST, request.FILES)
        if form.is_valid():
            new_association_goal = AssociationGoals(association=form.cleaned_data.get('association'),
                                                    goal=form.cleaned_data.get('goal'),
                                                    is_active=form.cleaned_data.get('is_active'),
                                                    )
            new_association_goal.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_association_goal',
                user=str(user.username),
                thing=str(new_association_goal.association.association_name)
            )
            new_log.save()
            return redirect('admin-panel-association-goals-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-association-goal.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteAssociationGoals(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        goal = AssociationGoals.objects.filter(id=pk).first()
        context = {
            'goal': goal
        }
        return render(request, 'admin-panel/delete-association-goal.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        goal = AssociationGoals.objects.filter(id=pk).first()
        goal.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_association_goal',
            user=str(user.username),
            thing=str(goal.association.association_name)
        )
        new_log.save()
        return redirect('admin-panel-association-goals-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelAssociationCategoryListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            association_cat = AssociationsCategories.objects.all()
        else:
            association_cat = AssociationsCategories.objects.\
                filter(category_name__regex=search).all()
            if association_cat is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_association_cat = make_grope(association_cat, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(association_cat) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_association_cat) < len(association_cat):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(association_cat)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'association_cat': all_association_cat,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/association-categories.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            cat = AssociationsCategories.objects.filter(category_name__regex=search).all()
            if len(cat) < 1:
                index = int(int(page) - 1)
                all_cat = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(cat) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_cat) < len(cat):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(cat)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'associations': all_cat[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/association-categories.html', context)
            else:
                index = int(int(page) - 1)
                all_cat = make_grope(cat, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(cat) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_cat) < len(cat):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(cat)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'associations': all_cat[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/association-categories.html', context)
        return redirect('admin-panel-association-categories-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelAssociationCategoryChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association_cat = AssociationsCategories.objects.filter(id=pk).first()
        form = UpdateAssociationCategoriesForm(initial={
            'category_url': association_cat.category_url,
            'category_name': association_cat.category_name,
        })
        context = {
            'form': form,
            'pk': pk,
            'association_cat': association_cat
        }
        return render(request, 'admin-panel/change-association-category.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        association_cat = AssociationsCategories.objects.filter(id=pk).first()
        edit_form = UpdateAssociationCategoriesForm(request.POST, request.FILES, instance=association_cat)
        if edit_form.is_valid():
            category_name = edit_form.cleaned_data.get('category_name')
            category_url = edit_form.cleaned_data.get('category_url')
            association_cat.category_name = category_name
            association_cat.category_url = category_url
            association_cat.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_association_category',
                user=str(user.username),
                thing=str(association_cat.category_name)
            )
            new_log.save()
            return redirect('admin-panel-change-association-categories', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-association-category.html', context),

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewAssociationCategory(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAssociationCategoriesForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-association-category.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAssociationCategoriesForm(request.POST, request.FILES)
        if form.is_valid():
            new_association_cat = AssociationsCategories(category_name=form.cleaned_data.get('category_name'),
                                                         category_url=form.cleaned_data.get('category_url'),
                                                            )
            new_association_cat.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_association_category',
                user=str(user.username),
                thing=str(new_association_cat.category_name)
            )
            new_log.save()
            return redirect('admin-panel-association-categories-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-association-category.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteAssociationCategory(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        cat = AssociationsCategories.objects.filter(id=pk).first()
        context = {
            'cat': cat
        }
        return render(request, 'admin-panel/delete-association-catrgory.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        cat = AssociationsCategories.objects.filter(id=pk).first()
        cat.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_association_category',
            user=str(user.username),
            thing=str(cat.category_name)
        )
        new_log.save()
        return redirect('admin-panel-association-categories-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelScienceListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            science = ScienceSubjectModel.objects.all()
        else:
            science = ScienceSubjectModel.objects.\
                filter(title__regex=search).all()
            if science is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_science = make_grope(science, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(science) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_science) < len(science):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(science)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'science': all_science,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/science-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            science = ScienceSubjectModel.objects.filter(title__regex=search).all()
            if len(science) < 1:
                index = int(int(page) - 1)
                all_science = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(science) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_science) < len(science):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(science)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'science': all_science[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/science-list.html', context)
            else:
                index = int(int(page) - 1)
                all_science = make_grope(science, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(science) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_science) < len(science):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(science)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'science': all_science[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/science-list.html', context)
        return redirect('admin-panel-science-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelScienceChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        science = ScienceSubjectModel.objects.filter(id=pk).first()
        form = UpdateScienceForm(initial={
            'title': science.title,
            'url_title': science.url_title,
            'image_on_science_detail_page': science.image_on_science_detail_page.url,
            'image_on_science_list_page': science.image_on_science_list_page.url,
            'is_active': science.is_active,
            'text1': science.text1,
            'text2': science.text2,
            'text3': science.text3,
            'text4': science.text4,
            'text5': science.text5,
            'text6': science.text6,
            'text7': science.text7,
            'text8': science.text8,
        })
        context = {
            'form': form,
            'pk': pk,
            'science': science
        }
        return render(request, 'admin-panel/change-science.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        science = ScienceSubjectModel.objects.filter(id=pk).first()
        edit_form = UpdateScienceForm(request.POST, request.FILES, instance=science)
        if edit_form.is_valid():
            science.title = edit_form.cleaned_data.get('title')
            science.url_title = edit_form.cleaned_data.get('url_title')
            science.is_active = edit_form.cleaned_data.get('is_active')
            science.image_on_science_list_page = edit_form.cleaned_data.get('image_on_science_list_page')
            science.image_on_science_detail_page = edit_form.cleaned_data.get('image_on_science_detail_page')
            science.text1 = edit_form.cleaned_data.get('text1')
            science.text2 = edit_form.cleaned_data.get('text2')
            science.text3 = edit_form.cleaned_data.get('text3')
            science.text4 = edit_form.cleaned_data.get('text4')
            science.text5 = edit_form.cleaned_data.get('text5')
            science.text6 = edit_form.cleaned_data.get('text6')
            science.text7 = edit_form.cleaned_data.get('text7')
            science.text8 = edit_form.cleaned_data.get('text8')
            science.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_science',
                user=str(user.username),
                thing=str(science.title)
            )
            new_log.save()
            return redirect('admin-panel-change-science', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-science.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewScience(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateScienceForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-science.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateScienceForm(request.POST, request.FILES)
        if form.is_valid():
            new_science = ScienceSubjectModel(title=form.cleaned_data.get('title'),
                                              url_title=form.cleaned_data.get('url_title'),
                                              is_active=form.cleaned_data.get('is_active'),
                                              image_on_science_list_page=form.cleaned_data.
                                              get('image_on_science_list_page'),
                                              image_on_science_detail_page=form.cleaned_data.
                                              get('image_on_science_detail_page'),
                                              text1=form.cleaned_data.get('text1'),
                                              text2=form.cleaned_data.get('text2'),
                                              text3=form.cleaned_data.get('text3'),
                                              text4=form.cleaned_data.get('text4'),
                                              text5=form.cleaned_data.get('text5'),
                                              text6=form.cleaned_data.get('text6'),
                                              text7=form.cleaned_data.get('text7'),
                                              text8=form.cleaned_data.get('text8'),)
            new_science.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_science',
                user=str(user.username),
                thing=str(new_science.title)
            )
            new_log.save()
            return redirect('admin-panel-science-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-science.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteScience(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        science = ScienceSubjectModel.objects.filter(id=pk).first()
        context = {
            'science': science
        }
        return render(request, 'admin-panel/delete-science.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        science = ScienceSubjectModel.objects.filter(id=pk).first()
        science.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_science',
            user=str(user.username),
            thing=str(science.title)
        )
        new_log.save()
        return redirect('admin-panel-science-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelNewsListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            news = NewsModel.objects.all()
        else:
            news = NewsModel.objects.\
                filter(title__regex=search).all()
            if news is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_news = make_grope(news, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(news) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_news) < len(news):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(news)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'news': all_news,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/news-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            news = NewsModel.objects.filter(title__regex=search).all()
            if len(news) < 1:
                index = int(int(page) - 1)
                all_news = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(news) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_news) < len(news):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(news)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'news': all_news[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/science-list.html', context)
            else:
                index = int(int(page) - 1)
                all_news = make_grope(news, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(news) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_news) < len(news):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(news)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'news': all_news[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/news-list.html', context)
        return redirect('admin-panel-news-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelNewsChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        news = NewsModel.objects.filter(id=pk).first()
        form = UpdateNewsForm(initial={
            'title': news.title,
            'url_title': news.url_title,
            'image_on_news_detail_page': news.image_on_news_detail_page.url,
            'image_on_news_list_page': news.image_on_news_list_page.url,
            'is_active': news.is_active,
            'text1': news.text1,
            'text2': news.text2,
            'text3': news.text3,
            'text4': news.text4,
            'text5': news.text5,
            'text6': news.text6,
            'text7': news.text7,
            'text8': news.text8,
            'show_on_index_page': news.show_on_index_page,
            'date': news.date
        })
        context = {
            'form': form,
            'pk': pk,
            'news': news
        }
        return render(request, 'admin-panel/change-news.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        news = NewsModel.objects.filter(id=pk).first()
        edit_form = UpdateNewsForm(request.POST, request.FILES, instance=news)
        if edit_form.is_valid():
            news.title = edit_form.cleaned_data.get('title')
            news.url_title = edit_form.cleaned_data.get('url_title')
            news.is_active = edit_form.cleaned_data.get('is_active')
            news.image_on_news_detail_page = edit_form.cleaned_data.get('image_on_news_detail_page')
            news.image_on_news_list_page = edit_form.cleaned_data.get('image_on_news_list_page')
            news.text1 = edit_form.cleaned_data.get('text1')
            news.text2 = edit_form.cleaned_data.get('text2')
            news.text3 = edit_form.cleaned_data.get('text3')
            news.text4 = edit_form.cleaned_data.get('text4')
            news.text5 = edit_form.cleaned_data.get('text5')
            news.text6 = edit_form.cleaned_data.get('text6')
            news.text7 = edit_form.cleaned_data.get('text7')
            news.text8 = edit_form.cleaned_data.get('text8')
            news.date = edit_form.cleaned_data.get('date')
            news.show_on_index_page = edit_form.cleaned_data.get(('show_on_index_page'))
            news.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_news',
                user=str(user.username),
                thing=str(news.title)
            )
            new_log.save()
            return redirect('admin-panel-change-news', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-news.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewNews(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateNewsForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-news.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateNewsForm(request.POST, request.FILES)
        if form.is_valid():
            new_news = NewsModel(title=form.cleaned_data.get('title'),
                                 url_title=form.cleaned_data.get('url_title'),
                                 is_active=form.cleaned_data.get('is_active'),
                                 image_on_news_list_page=form.cleaned_data.get('image_on_news_list_page'),
                                 image_on_news_detail_page=form.cleaned_data.get('image_on_news_detail_page'),
                                 text1=form.cleaned_data.get('text1'),
                                 text2=form.cleaned_data.get('text2'),
                                 text3=form.cleaned_data.get('text3'),
                                 text4=form.cleaned_data.get('text4'),
                                 text5=form.cleaned_data.get('text5'),
                                 text6=form.cleaned_data.get('text6'),
                                 text7=form.cleaned_data.get('text7'),
                                 text8=form.cleaned_data.get('text8'),
                                 date=form.cleaned_data.get('date'),
                                 show_on_index_page=form.cleaned_data.get('show_on_index_page')
                                 )
            new_news.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_news',
                user=str(user.username),
                thing=str(new_news.title)
            )
            new_log.save()
            return redirect('admin-panel-news-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-news.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteNews(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        news = NewsModel.objects.filter(id=pk).first()
        context = {
            'news': news
        }
        return render(request, 'admin-panel/delete-news.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        news = NewsModel.objects.filter(id=pk).first()
        news.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_news',
            user=str(user.username),
            thing=str(news.title)
        )
        new_log.save()
        return redirect('admin-panel-news-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelUserListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            users = User.objects.all()
        else:
            users = User.objects.filter(username__iregex=search).all()
            if users is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_users = make_grope(users, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(users) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_users) < len(users):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(users)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'users': all_users,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/user-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            users = User.objects.filter(username__iregex=search).all()
            if len(users) < 1:
                index = int(int(page) - 1)
                all_users = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(users) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_users) < len(users):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(users)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'users'
                    '': all_users[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/user-list.html', context)
            else:
                index = int(int(page) - 1)
                all_users = make_grope(users, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(users) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_users) < len(users):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(users)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'users': all_users[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/user-list.html', context)
        return redirect('admin-panel-user-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelMainSettingListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            setting = SiteSettingModel.objects.all()
        else:
            setting = SiteSettingModel.objects.\
                filter(site_setting_name__regex=search).all()
            if setting is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_setting = make_grope(setting, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(setting) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_setting) < len(setting):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(setting)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'setting': all_setting,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/main-site-setting-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            setting = SiteSettingModel.objects.filter(site_setting_name__regex=search).all()
            if len(setting) < 1:
                index = int(int(page) - 1)
                all_setting = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(setting) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_setting) < len(setting):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(setting)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'setting': all_setting[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/main-site-setting-list.html', context)
            else:
                index = int(int(page) - 1)
                all_setting = make_grope(setting, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(setting) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_setting) < len(setting):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(setting)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'setting': all_setting[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/main-site-setting-list.html', context)
        return redirect('admin-panel-main-setting-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelMainSettingChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        setting = SiteSettingModel.objects.filter(id=pk).first()
        form = UpdateMainSettingForm(initial={
            'site_setting_name': setting.site_setting_name,
            'site_logo_2': setting.site_logo_2.url,
            'site_logo_1': setting.site_logo_1.url,
            'is_active': setting.is_active,
            'any_button': setting.any_button,
            'decoration': setting.decoration,
            'footer_text': setting.footer_text,
            'footer_phone_number': setting.footer_phone_number,
            'facebook_link': setting.facebook_link,
            'instagram_link': setting.instagram_link,
            'twitter_link': setting.twitter_link,
            'button_link': setting.button_link,
            'button_text': setting.button_text,
            'under_h1_text': setting.under_h1_text,
            'h1_text_main_page': setting.h1_text_main_page
        })
        context = {
            'form': form,
            'pk': pk,
            'setting': setting
        }
        return render(request, 'admin-panel/change-main-setting.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        setting = SiteSettingModel.objects.filter(id=pk).first()
        edit_form = UpdateMainSettingForm(request.POST, request.FILES, instance=setting)
        if edit_form.is_valid():
            setting.site_setting_name = edit_form.cleaned_data.get('site_setting_name')
            setting.h1_text_main_page = edit_form.cleaned_data.get('h1_text_main_page')
            setting.under_h1_text = edit_form.cleaned_data.get('under_h1_text')
            setting.button_text = edit_form.cleaned_data.get('button_text')
            setting.button_link = edit_form.cleaned_data.get('button_link')
            setting.twitter_link = edit_form.cleaned_data.get('twitter_link')
            setting.instagram_link = edit_form.cleaned_data.get('instagram_link')
            setting.facebook_link = edit_form.cleaned_data.get('facebook_link')
            setting.footer_phone_number = edit_form.cleaned_data.get('footer_phone_number')
            setting.footer_text = edit_form.cleaned_data.get('footer_text')
            setting.decoration = edit_form.cleaned_data.get('decoration')
            setting.any_button = edit_form.cleaned_data.get('any_button')
            setting.is_active = edit_form.cleaned_data.get('is_active')
            setting.site_logo_1 = edit_form.cleaned_data.get('site_logo_1')
            setting.site_logo_2 = edit_form.cleaned_data.get('site_logo_2')
            setting.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_main_setting',
                user=str(user.username),
                thing=str(setting.site_setting_name)
            )
            new_log.save()
            return redirect('admin-panel-change-main-setting', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-main-setting.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewMainSetting(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateMainSettingForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-main-setting.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateMainSettingForm(request.POST, request.FILES)
        if form.is_valid():
            new_setting = SiteSettingModel(site_setting_name=form.cleaned_data.get('site_setting_name'),
                                           h1_text_main_page=form.cleaned_data.get('h1_text_main_page'),
                                           under_h1_text=form.cleaned_data.get('under_h1_text'),
                                           button_text=form.cleaned_data.get('button_text'),
                                           button_link=form.cleaned_data.get('button_link'),
                                           twitter_link=form.cleaned_data.get('twitter_link'),
                                           instagram_link=form.cleaned_data.get('instagram_link'),
                                           facebook_link=form.cleaned_data.get('facebook_link'),
                                           footer_phone_number=form.cleaned_data.get('footer_phone_number'),
                                           footer_text=form.cleaned_data.get('footer_text'),
                                           decoration=form.cleaned_data.get('decoration'),
                                           any_button=form.cleaned_data.get('any_button'),
                                           is_active=form.cleaned_data.get('is_active'),
                                           site_logo_1=form.cleaned_data.get('site_logo_1'),
                                           site_logo_2=form.cleaned_data.get('site_logo_2'),)
            new_setting.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_main_setting',
                user=str(user.username),
                thing=str(new_setting.site_setting_name)
            )
            new_log.save()
            return redirect('admin-panel-main-setting-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-main-setting.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteMainSetting(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        setting = SiteSettingModel.objects.filter(id=pk).first()
        context = {
            'setting': setting
        }
        return render(request, 'admin-panel/delete-main-setting.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        setting = SiteSettingModel.objects.filter(id=pk).first()
        setting.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_main_setting',
            user=str(user.username),
            thing=str(setting.site_setting_name)
        )
        new_log.save()
        return redirect('admin-panel-main-setting-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelAboutUsListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            about_us = AboutUsModel.objects.all()
        else:
            about_us = AboutUsModel.objects.\
                filter(name__iregex=search).all()
            if about_us is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_about_us = make_grope(about_us, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(about_us) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_about_us) < len(about_us):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(about_us)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'about_us': all_about_us,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/about-us-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            about_us = AboutUsModel.objects.filter(name__regex=search).all()
            if len(about_us) < 1:
                index = int(int(page) - 1)
                all_about_us = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(about_us) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_about_us) < len(about_us):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(about_us)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'about_us': all_about_us[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/about-us-list.html', context)
            else:
                index = int(int(page) - 1)
                all_about_us = make_grope(about_us, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(about_us) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_about_us) < len(about_us):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(about_us)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'about_us': all_about_us[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/about-us-list.html', context)
        return redirect('admin-panel-about-us-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelAboutUsChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        about_us = AboutUsModel.objects.filter(id=pk).first()
        form = UpdateAboutUsForm(initial={
            'name': about_us.name,
            'phone_number': about_us.phone_number,
            'address': about_us.address,
            'main_text': about_us.main_text,
            'second_text': about_us.second_text,
            'is_active': about_us.is_active,
        })
        context = {
            'form': form,
            'pk': pk,
            'about_us': about_us
        }
        return render(request, 'admin-panel/change-about-us.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        about_us = AboutUsModel.objects.filter(id=pk).first()
        edit_form = UpdateAboutUsForm(request.POST, request.FILES, instance=about_us)
        if edit_form.is_valid():
            about_us.name = edit_form.cleaned_data.get('name')
            about_us.address = edit_form.cleaned_data.get('address')
            about_us.phone_number = edit_form.cleaned_data.get('phone_number')
            about_us.main_text = edit_form.cleaned_data.get('main_text')
            about_us.second_text = edit_form.cleaned_data.get('second_text')
            about_us.is_active = edit_form.cleaned_data.get('is_active')
            about_us.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_about_us',
                user=str(user.username),
                thing=str(about_us.name)
            )
            new_log.save()
            return redirect('admin-panel-change-about-us', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-about-us.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewAboutUs(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAboutUsForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-about-us.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateAboutUsForm(request.POST, request.FILES)
        if form.is_valid():
            new_about_us = AboutUsModel(name=form.cleaned_data.get('name'),
                                        address=form.cleaned_data.get('address'),
                                        phone_number=form.cleaned_data.get('phone_number'),
                                        main_text=form.cleaned_data.get('main_text'),
                                        second_text=form.cleaned_data.get('second_text'),
                                        is_active=form.cleaned_data.get('is_active'),

                                        )
            new_about_us.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_about_us',
                user=str(user.username),
                thing=str(new_about_us.name)
            )
            new_log.save()
            return redirect('admin-panel-about-us-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-about-us.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteAboutUs(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        about_us = AboutUsModel.objects.filter(id=pk).first()
        context = {
            'about_us': about_us
        }
        return render(request, 'admin-panel/delete-about-us.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        about_us = AboutUsModel.objects.filter(id=pk).first()
        about_us.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_about_us',
            user=str(user.username),
            thing=str(about_us.name)
        )
        new_log.save()
        return redirect('admin-panel-about-us-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelFooterCategoryListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            footer_cat = FooterBoxCategoryModel.objects.all()
        else:
            footer_cat = FooterBoxCategoryModel.objects.\
                filter(category_name__regex=search).all()
            if footer_cat is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_footer_cat = make_grope(footer_cat, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(footer_cat) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_footer_cat) < len(footer_cat):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(footer_cat)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'footer_cat': all_footer_cat,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/footer-category-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            footer_cat = FooterBoxCategoryModel.objects.filter(category_name__regex=search).all()
            if len(footer_cat) < 1:
                index = int(int(page) - 1)
                all_footer_cat = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(footer_cat) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_footer_cat) < len(footer_cat):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(footer_cat)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'footer_cat': all_footer_cat[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/footer-category-list.html', context)
            else:
                index = int(int(page) - 1)
                all_footer_cat = make_grope(footer_cat, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(footer_cat) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_footer_cat) < len(footer_cat):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(footer_cat)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'footer_cat': all_footer_cat[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/footer-category-list.html', context)
        return redirect('admin-panel-footer-category-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelFooterCategoryChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_cat = FooterBoxCategoryModel.objects.filter(id=pk).first()
        form = UpdateFooterCategoryForm(initial={
            'category_name': footer_cat.category_name,
            'url': footer_cat.url,
        })
        context = {
            'form': form,
            'pk': pk,
            'footer_cat': footer_cat
        }
        return render(request, 'admin-panel/change-footer-category.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_cat = FooterBoxCategoryModel.objects.filter(id=pk).first()
        edit_form = UpdateFooterCategoryForm(request.POST, request.FILES, instance=footer_cat)
        if edit_form.is_valid():
            footer_cat.category_name = edit_form.cleaned_data.get('category_name')
            footer_cat.url = edit_form.cleaned_data.get('url')
            footer_cat.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_footer_category',
                user=str(user.username),
                thing=str(footer_cat.category_name)
            )
            new_log.save()
            return redirect('admin-panel-change-footer-category', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-footer-category.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewFooterCategory(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateFooterCategoryForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-footer-category.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateFooterCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            new_footer_cat = FooterBoxCategoryModel(category_name=form.cleaned_data.get('category_name'),
                                                    url=form.cleaned_data.get('url'),)
            new_footer_cat.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_footer_category',
                user=str(user.username),
                thing=str(new_footer_cat.category_name)
            )
            new_log.save()
            return redirect('admin-panel-footer-category-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-footer-category.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteFooterCategory(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_cat = FooterBoxCategoryModel.objects.filter(id=pk).first()
        context = {
            'footer_cat': footer_cat
        }
        return render(request, 'admin-panel/delete-footer-category.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_cat = FooterBoxCategoryModel.objects.filter(id=pk).first()
        footer_cat.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_footer_category',
            user=str(user.username),
            thing=str(footer_cat.category_name)
        )
        new_log.save()
        return redirect('admin-panel-footer-category-list', 'all', 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelFooterSubCategoryListView(View):
    def get(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        is_search_none = False
        if search == 'all':
            footer_sub_cat = FooterBoxSubModel.objects.all()
        else:
            footer_sub_cat = FooterBoxSubModel.objects.\
                filter(title__regex=search).all()
            if footer_sub_cat is None:
                is_search_none = True
        index = int(int(page) - 1)
        all_footer_sub_cat = make_grope(footer_sub_cat, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(footer_sub_cat) / paginate_by + 1)
        page_range = range(1, page_count)
        if len(all_footer_sub_cat) < len(footer_sub_cat):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(footer_sub_cat)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        form = SearchBoxForm
        context = {
            'footer_sub_cat': all_footer_sub_cat,
            'form': form,
            'search': search,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range[::-1],
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
            'is_search_none': is_search_none
        }
        return render(request, 'admin-panel/footer-sub-link-list.html', context)

    def post(self, request, search, page):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search_box')
            footer_sub_cat = FooterBoxSubModel.objects.filter(category_name__regex=search).all()
            if len(footer_sub_cat) < 1:
                index = int(int(page) - 1)
                all_footer_sub_cat = []
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(footer_sub_cat) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_footer_sub_cat) < len(footer_sub_cat):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(footer_sub_cat)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'footer_sub_cat': all_footer_sub_cat[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number,
                }
                return render(request, 'admin-panel/footer-sub-link-list.html', context)
            else:
                index = int(int(page) - 1)
                all_footer_sub_cat = make_grope(footer_sub_cat, paginate_by)[index]
                has_other_pages = False
                current_page = int(page)
                page_count = int(len(footer_sub_cat) / paginate_by + 1)
                page_range = range(1, page_count)
                if len(all_footer_sub_cat) < len(footer_sub_cat):
                    has_other_pages = True
                has_previous = False
                has_next = True
                previous_page_number = int(page) - 1
                next_page_number = int(page) + 1
                if int(page) > 1:
                    has_previous = True
                last_page = int(len(footer_sub_cat)) / paginate_by
                if float(page) >= float(last_page):
                    has_next = False
                form = SearchBoxForm
                context = {
                    'footer_sub_cat': all_footer_sub_cat[::-1],
                    'form': form,
                    'search': search,
                    'has_other_page': has_other_pages,
                    'current_page': current_page,
                    'page_range': page_range[::-1],
                    'has_previous': has_previous,
                    'previous_page_number': previous_page_number,
                    'has_next': has_next,
                    'next_page_number': next_page_number
                }
                return render(request, 'admin-panel/footer-sub-link-list.html', context)
        return redirect('admin-panel-footer-sub-category-list', search, 1)

@method_decorator(login_required, 'dispatch')
class AdminPanelFooterSubCategoryChangeView(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_sub_cat = FooterBoxSubModel.objects.filter(id=pk).first()
        form = UpdateFooterSubCategoryForm(initial={
            'link': footer_sub_cat.link,
            'category': footer_sub_cat.category,
            'title': footer_sub_cat.title
        })
        context = {
            'form': form,
            'pk': pk,
            'footer_sub_cat': footer_sub_cat
        }
        return render(request, 'admin-panel/change-footer-sub-link.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_sub_cat = FooterBoxSubModel.objects.filter(id=pk).first()
        edit_form = UpdateFooterSubCategoryForm(request.POST, request.FILES, instance=footer_sub_cat)
        if edit_form.is_valid():
            footer_sub_cat.category = edit_form.cleaned_data.get('category')
            footer_sub_cat.link = edit_form.cleaned_data.get('link')
            footer_sub_cat.title = edit_form.cleaned_data.get('title')
            footer_sub_cat.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='change_footer_sub_category',
                user=str(user.username),
                thing=str(footer_sub_cat.title)
            )
            new_log.save()
            return redirect('admin-panel-change-footer-sub-category', pk)

        context = {
            'form': edit_form,
            'pk': pk,
        }
        return render(request, 'admin-panel/change-footer-sub-link.html', context)

@method_decorator(login_required, 'dispatch')
class AdminPanelCreateNewFooterSubCategory(View):
    def get(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateFooterSubCategoryForm
        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-footer-sub-link.html', context)

    def post(self, request):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        form = UpdateFooterSubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            new_footer_sub_cat = FooterBoxSubModel(category=form.cleaned_data.get('category'),
                                                   title=form.cleaned_data.get('title'),
                                                   link=form.cleaned_data.get('link'))
            new_footer_sub_cat.save()
            user = request.user
            new_log = AdminPanelLogModel(
                date=datetime.date.today(),
                time=datetime.time,
                type='new_footer_sub_category',
                user=str(user.username),
                thing=str(new_footer_sub_cat.title)
            )
            new_log.save()
            return redirect('admin-panel-footer-sub-category-list', 'all', 1)

        context = {
            "form": form
        }
        return render(request, 'admin-panel/new-footer-sub-link.html', context)

@method_decorator(login_required, 'dispatch')
class DeleteFooterSubCategory(View):
    def get(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_sub_cat = FooterBoxSubModel.objects.filter(id=pk).first()
        context = {
            'footer_sub_cat': footer_sub_cat
        }
        return render(request, 'admin-panel/delete-footer-sub-link.html', context)

    def post(self, request, pk):
        user = request.user
        if not user.is_staff :
            return render(request , '404/404.html')
        footer_sub_cat = FooterBoxSubModel.objects.filter(id=pk).first()
        footer_sub_cat.delete()
        user = request.user
        new_log = AdminPanelLogModel(
            date=datetime.date.today(),
            time=datetime.time,
            type='delete_footer_sub_category',
            user=str(user.username),
            thing=str(footer_sub_cat.title)
        )
        new_log.save()
        return redirect('admin-panel-footer-sub-category-list', 'all', 1)
