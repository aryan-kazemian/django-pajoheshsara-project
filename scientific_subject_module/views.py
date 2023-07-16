from django.shortcuts import render
from .models import ScienceSubjectModel
from functions.functions import make_grope

# Create your views here.

paginate_by = 3

def science_list(request, page):
    science = ScienceSubjectModel.objects.filter(is_active=True).all()
    index = int(int(page) - 1)
    all_sciences = make_grope(science, paginate_by)[index]
    has_other_pages = False
    current_page = int(page)
    page_count = int(len(science) / paginate_by + 1)
    page_range = range(1, page_count)
    if len(all_sciences) < len(science):
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
    context = {
        'all_science': all_sciences,
        'has_other_page': has_other_pages,
        'current_page': current_page,
        'page_range': page_range,
        'has_previous': has_previous,
        'previous_page_number': previous_page_number,
        'has_next': has_next,
        'next_page_number': next_page_number,
    }
    return render(request, 'science_module/science_list.html', context)

def science_detail(request, science_url):
    science = ScienceSubjectModel.objects.get(url_title__iexact=science_url)
    context = {
        'science': science
    }
    return render(request, 'science_module/science-details.html', context)
