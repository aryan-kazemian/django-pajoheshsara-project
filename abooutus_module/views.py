from django.shortcuts import render
from django.views.generic import TemplateView
from .models import AboutUsModel

# Create your views here.

class AboutUsTemplateView(TemplateView):
    template_name = 'aboutus/about-us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsTemplateView, self).get_context_data(**kwargs)
        about_us_setting =AboutUsModel.objects.filter(is_active=True).first()
        context['setting'] = about_us_setting
        return context
