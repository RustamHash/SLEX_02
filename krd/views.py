from django.http import HttpResponse
from django.shortcuts import render
from base_app.apps import option_dict

from base_app.models import Menu, Contracts
from rnd.contract_models import neo_stroy_krd, ok


slug_filial = str(__name__).split('.')[0]
context = {
    'prefix': slug_filial,
    'title': option_dict[slug_filial]
}
dict_module = {
    'neo-stroj-rostov': neo_stroy_krd,
    'ok': ok,
}


def home(request):
    context['menu'] = Menu.objects.filter(as_active=True, filial__slug=slug_filial)
    return render(request, f'{slug_filial}/home.html', context=context)


def view_contracts(request):
    context['contracts'] = Contracts.objects.filter(as_active=True, filial__slug=slug_filial)
    return render(request, f'{slug_filial}/contracts.html', context=context)


def contract(request, slug):
    context['contract'] = Contracts.objects.get(as_active=True, filial__slug=slug_filial, slug=slug)
    return render(request, f'{slug_filial}/contract_menu.html', context=context)


def load_order(request, contr_slug):
    if request.method == 'POST':
        file = request.FILES.get('file', False)
        if file:
            queryset = Contracts.objects.get(slug=contr_slug)
            print(queryset)
            # res, error_valid = dict_module[slug].start(file, queryset)
            # if not error_valid:
            #     return HttpResponse(f'Ошибка обработки\n{res}')
            # context['result'] = res
            # return render(request, 'krd/contract_menu.html', context=context)
    return HttpResponse('Файл не выбран!')
