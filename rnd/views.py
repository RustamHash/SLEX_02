from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from base_app.apps import option_dict

from base_app.models import Menu, Contracts
from base_app.pg_utils import get_good_by_marking_goods, get_goods_list_by_marking_goods, \
    query_goods_stock_by_group_id_ok, query_goods_stock_by_group_id

from rnd.contract_models import ok, neo_stroy_krd

slug_filial = str(__name__).split('.')[0]
context = {
    'prefix': slug_filial,
    'title': option_dict[slug_filial]
}


def home(request):
    context['menu'] = Menu.objects.filter(as_active=True, filial__slug=slug_filial)
    return render(request, f'base_app/home.html', context=context)


def contracts_list(request):
    context['contracts'] = Contracts.objects.filter(as_active=True, filial__slug=slug_filial)
    return render(request, f'base_app/contracts.html', context=context)


def contract_detail(request, slug):
    context['contract'] = Contracts.objects.get(as_active=True, filial__slug=slug_filial, slug=slug)
    return render(request, f'{slug_filial}/contract_menu.html', context=context)
