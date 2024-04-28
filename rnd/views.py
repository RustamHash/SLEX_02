from django.http import HttpResponse
from django.shortcuts import render
from base_app.apps import option_dict

slug_filial = str(__name__).split('.')[0]
context = {
    'prefix': slug_filial,
    'title': option_dict[slug_filial]
}


def home(request):
    return render(request, f'{slug_filial}/home.html', context=context)
