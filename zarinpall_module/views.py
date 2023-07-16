from django.shortcuts import render
from django.views import View

def zarin_pall(request, course_name):
    # todo : dargah pardakht
    context = {
        'text': 'خرید از درگاه پرداخت زرین پال',
        'course_name': course_name
    }
    return render(request, 'zarinpall_module/zarinpall.html', context)

