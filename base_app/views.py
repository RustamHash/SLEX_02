from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect

from base_app.models import Filial, Contracts, Menu

from base_app.pg_utils import get_good_by_marking_goods, get_goods_list_by_marking_goods, \
    query_goods_stock_by_group_id_ok, query_goods_stock_by_group_id

from base_app.contract_models import neo_stroy_krd
from base_app.contract_models.rnd import ok

context = {
    'title': 'Главная'
}
dict_module = {
    'neo-stroj-rostov': neo_stroy_krd,
    'ok': ok,
}

filial_slug = ''


def home(request):
    context.clear()
    context['filial'] = Filial.objects.filter(as_active=True)
    return render(request, 'base_app/home.html', context=context)


def home_filial(request, _filial_slug):
    global filial_slug
    filial_slug = _filial_slug
    context['menu'] = Menu.objects.filter(as_active=True, filial__slug=filial_slug)
    return render(request, f'base_app/home_filial.html', context=context)


def list_view_contracts(request, _filial_slug):
    context['contracts'] = Contracts.objects.filter(as_active=True, filial__slug=filial_slug)
    return render(request, f'base_app/contracts.html', context=context)


def detail_view_contracts(request, _contract_slug, _filial_slug):
    context['result'] = False
    context['contract'] = Contracts.objects.get(as_active=True, filial__slug=filial_slug, slug=_contract_slug)
    return render(request, f'base_app/contract_menu.html', context=context)


def load_order(request, _contract_slug, _filial_slug):
    if request.method == 'POST':
        context['error_msg'] = False
        context['msg'] = False
        file = request.FILES.get('file', False)
        if file:
            _contract = Contracts.objects.get(filial__slug=_filial_slug, slug=_contract_slug)
            res, error_valid = dict_module[_contract_slug].start(file, _contract)
            print(f'error_valid_{error_valid}')
            if error_valid:
                context['msg'] = f'Ошибка обработки\n{res}'
                context['error_msg'] = True
                return render(request, f'base_app/contract_menu.html', context=context)
            context['msg'] = f'Успешно!'
            context['error_msg'] = False
            context['result'] = res
            return render(request, f'base_app/contract_menu.html', context=context)
    else:
        context['error_msg'] = True
    return render(request, f'base_app/contract_menu.html', context=context)


def check_one_goods_in_pg(request, contract_slug):
    if request.method == 'POST':
        marking = request.POST.get('marking', False)
        if marking:
            _contract = Contracts.objects.get(filial__slug=filial_slug, slug=contract_slug)
            _df_res = get_good_by_marking_goods(_marking_goods=int(marking), _contract=_contract)
            context['_df_res'] = _df_res
            return render(request, f'base_app/contract_menu.html', context=context)


def check_all_goods_in_pg(request, contract_slug):
    if request.method == 'POST':
        file = request.FILES.get('file', False)
        if file:
            _contract = Contracts.objects.get(filial__slug=filial_slug, slug=contract_slug)
            _df_res = get_goods_list_by_marking_goods(_file_marking_goods=file, _contract=_contract)
            context['_df_res'] = _df_res
            return render(request, f'base_app/contract_menu.html', context=context)


def get_stock_store_by_group_id_contract(request, contract_slug):
    _contract = Contracts.objects.get(filial__slug=filial_slug, slug=contract_slug)
    group_id = _contract.id_groups_goods
    if contract_slug == 'ok':
        _df_res = query_goods_stock_by_group_id_ok(id_group_goods=group_id, _contract=_contract)
    else:
        _df_res = query_goods_stock_by_group_id(id_group_goods=group_id, _contract=_contract)
    context['_df_res'] = _df_res
    return render(request, f'base_app/contract_menu.html', context=context)


class Login(LoginView):
    template_name = 'base_app/login.html'

    def get_success_url(self):
        return super(Login, self).get_success_url()


class NotFound(LoginView):
    template_name = 'base_app/not_groups.html'

    def get_success_url(self):
        return super(NotFound, self).get_success_url()


def logout_view(request):
    logout(request)
    return redirect('home')
