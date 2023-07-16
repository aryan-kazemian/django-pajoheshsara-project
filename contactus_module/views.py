from django.shortcuts import render , redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import ContactUsForm
from .models import ContactUsModel
from django.views.generic import CreateView

# Create your views here.

class ContactUsView(View):
    def get(self, request):
        form = ContactUsForm
        context = {
            'form': form
        }
        return render(request, 'contactus_module/contactus.html', context)

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            new_contact = ContactUsModel(
                name=request.POST['name'],
                subject=request.POST['subject'],
                text=request.POST['text']
            )
            new_contact.save()
            return redirect('index-page-alert', alert='alert-from-contactus')
        else:
            context = {
                'form': form
            }
            return render(request, 'contactus_module/contactus.html', context)

