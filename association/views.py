from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from .models import AssociationModel, AssociationsCategories
from .forms import SearchBoxForm
from functions.functions import *

# Create your views here.

paginate_by = 4

class AssociationView(View):
    def get(self, request, page):
        form = SearchBoxForm
        associations = AssociationModel.objects.filter(is_active=True).all()
        categories = AssociationsCategories.objects.all()
        index = int(int(page) - 1)
        all_associations = make_grope(associations, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(associations) / paginate_by + 1)
        page_range = range(1, page_count + 1)
        if len(all_associations) < len(associations):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(associations)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        context = {
            'all_associations': all_associations,
            'categories': categories,
            'form': form,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range,
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,
        }
        return render(request, 'association_module/all_associations.html', context)

    def post(self, request, page):
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search_box = form.cleaned_data.get('search_box')
            all_associations = AssociationModel.objects.filter(association_name__regex=search_box)
        else:
            all_associations = AssociationModel.objects.filter(is_active=True).all()
        categories = AssociationsCategories.objects.all()
        context = {
            'all_associations': all_associations,
            'categories': categories,
            'form': form
        }
        return render(request, 'association_module/all_associations.html', context)


class AssociationFilter(View):
    def get(self, request, category, page):
        form = SearchBoxForm
        cat = category
        categories = AssociationsCategories.objects.all()
        associations = AssociationModel.objects.filter(is_active=True, association_category__category_url__iexact=cat)\
            .all()
        current_cat = associations[0].association_category.category_name
        index = int(int(page) - 1)
        all_associations = make_grope(associations, paginate_by)[index]
        has_other_pages = False
        current_page = int(page)
        page_count = int(len(associations) / paginate_by + 1)
        page_range = range(1, page_count + 1)
        if len(all_associations) < len(associations):
            has_other_pages = True
        has_previous = False
        has_next = True
        previous_page_number = int(page) - 1
        next_page_number = int(page) + 1
        if int(page) > 1:
            has_previous = True
        last_page = int(len(associations)) / paginate_by
        if float(page) >= float(last_page):
            has_next = False
        context = {
            'all_associations': all_associations,
            'categories': categories,
            'form': form,
            'current_category': current_cat,
            'has_other_page': has_other_pages,
            'current_page': current_page,
            'page_range': page_range,
            'has_previous': has_previous,
            'previous_page_number': previous_page_number,
            'has_next': has_next,
            'next_page_number': next_page_number,

        }
        return render(request, 'association_module/all_associations.html', context)

    def post(self, request, page):
        form = SearchBoxForm(request.POST)
        if form.is_valid():
            search_box = form.cleaned_data.get('search_box')
            all_associations = AssociationModel.objects.filter(association_name__regex=search_box)
        else:
            all_associations = AssociationModel.objects.filter(is_active=True).all()
        categories = AssociationsCategories.objects.all()
        context = {
            'all_associations': all_associations,
            'categories': categories,
            'form': form,
        }
        return render(request, 'association_module/all_associations.html', context)

def association_detail(request, association):
    association = AssociationModel.objects.get(association_name__iexact=association)
    related_associations = AssociationModel.objects.filter(association_category=association.association_category).all()
    context = {
        'association': association,
        'related_associations': related_associations
    }
    return render(request, 'association_module/association-detail.html', context)






