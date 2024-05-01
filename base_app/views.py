import pandas as pd
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect

from base_app.models import Filial, Contracts, Menu, Operations
from base_app.processing_utils import normalizing_of_start_function

from base_app.contract_models import neo_stroy_krd

from base_app.contract_models.rnd import ok

from base_app.contract_models.krd import toshev, kzvs, agro

from pg_sql.models import PgStocks, PgGoods
from wms_app.models import WmsStocks, WmsGoods

context = {}
dict_module = {
    'toshev-rf': toshev,
    'kzvs': kzvs,
    'neo-stroy-krd': neo_stroy_krd,
    'neo-stroy-sochi': neo_stroy_krd,
    'agrokompleks': agro,
    'neo-stroj-rostov': neo_stroy_krd,
}
dict_operation = {
    'order_btn': False,
    'check_goods_pg_btn': False,
    'stock_pg_btn': False,
    'stock_wms_btn': False,
}
dict_operation_btn = {
    'load_btn': False,
    'search_btn': False,
}


def home(request):
    context.clear()
    context['menus'] = Filial.objects.filter(as_active=True)
    return render(request, 'base_app/home.html', context=context)


def home_filial(request, _filial_slug):
    __clear_context()
    context['filial'] = Filial.objects.get(slug=_filial_slug)
    context['menus'] = Menu.objects.filter(as_active=True, filial__id=context['filial'].id)
    return render(request, f'base_app/home.html', context=context)


def show_contracts(request, **kwargs):
    __clear_context()
    context['menus'] = Contracts.objects.filter(as_active=True, filial__slug=context['filial'].slug)
    return render(request, f'base_app/home.html', context=context)


def show_operations(request, **kwargs):
    __clear_context()
    context['contract_selected'] = kwargs['_contract_slug']
    context['operations'] = Operations.objects.filter(as_active=True, contract__slug=kwargs['_contract_slug'])
    context['contract'] = Contracts.objects.get(filial__slug=context['filial'].slug, slug=kwargs['_contract_slug'])
    return render(request, f'base_app/operations.html', context=context)


def show_choice_operation(request, **kwargs):
    context['operation'] = Operations.objects.get(slug=kwargs['_operation_slug'])
    context['operation_selected'] = kwargs['_operation_slug']
    return render(request, f'base_app/operations.html', context=context)


def event_load_file(request, **kwargs):
    if kwargs['_contract_slug'] == 'ok':
        if kwargs['_operation_slug'] == 'check_goods_in_pg':
            _file = request.FILES['file']
            context['result'] = PgGoods().get_goods_list_by_marking_goods(_file_marking_goods=_file,
                                                                          _contract=context['contract'])
            try:
                return FileResponse(open(context['result'], 'rb'))
            except Exception as e:
                context['result'] = {'error': e}
    if request.method == 'POST':
        file = request.FILES.get('file', False)
        if file:
            res, error_valid = dict_module[context['contract'].slug].start(file, context['contract'])
            if not error_valid:
                if isinstance(res, dict):
                    context['result'] = res
                else:
                    context['result'] = {'error': f'Ошибка обработки\n{res}'}
                return render(request, f'base_app/show_result.html', context=context)
            context['result'] = res
            return render(request, f'base_app/show_result.html', context=context)
    return render(request, f'base_app/operations.html', context=context)


def event_search_goods(request, **kwargs):
    if request.method == 'POST':
        if kwargs['_operation_slug'] == 'check_goods_in_pg':
            if 'search_input' in request.POST:
                _marking_goods = request.POST['search_input']
                context['result'] = PgGoods().get_good_by_marking_goods(_marking_goods=str(_marking_goods),
                                                                        _contract=context['contract'])
            else:
                _file = request.FILES['file']
                context['result'] = PgGoods().get_goods_list_by_marking_goods(_file_marking_goods=_file,
                                                                              _contract=context['contract'])
            try:
                return FileResponse(open(context['result'], 'rb'))
            except Exception as e:
                context['result'] = {'error': e}
    return render(request, f'base_app/operations.html', context=context)


def event_load_stock(request, **kwargs):
    if request.method == 'POST':
        if kwargs['_operation_slug'] == 'load_stock_pg':
            context['result'] = PgStocks().query_goods_stock_by_group_id(_contract=context['contract'])
        elif kwargs['_operation_slug'] == 'load_stock_pg_ok':
            _file_name_list = PgStocks().query_goods_stock_by_group_id_ok(_contract=context['contract'])
            _dict_file_name = {}
            for _file_name in _file_name_list:
                _dict_file_name[_file_name] = 'Файл сохранен'
            context['result'] = _dict_file_name
            return render(request, f'base_app/show_result.html', context=context)
        elif kwargs['_operation_slug'] == 'load_stock_wms':
            context['result'] = WmsStocks().get_goods_by_guid_group(_contract=context['contract'], top=20)
        try:
            return FileResponse(open(context['result'], 'rb'))
        except Exception as e:
            context['result'] = {'error': e}
            return render(request, f'base_app/show_result.html', context=context)
    return render(request, f'base_app/operations.html', context=context)


# РФ17676F101

# def check_one_goods_in_pg(request, contract_slug):
#     if request.method == 'POST':
#         marking = request.POST.get('marking', False)
#         if marking:
#             _contract = Contracts.objects.get(filial__slug=filial_slug, slug=contract_slug)
#             _df_res = get_good_by_marking_goods(_marking_goods=int(marking), _contract=_contract)
#             context['_df_res'] = _df_res
#             return render(request, f'base_app/contract_menu.html', context=context)
#
#
# def check_all_goods_in_pg(request, contract_slug):
#     if request.method == 'POST':
#         file = request.FILES.get('file', False)
#         if file:
#             _contract = Contracts.objects.get(filial__slug=filial_slug, slug=contract_slug)
#             _df_res = get_goods_list_by_marking_goods(_file_marking_goods=file, _contract=_contract)
#             context['_df_res'] = _df_res
#             return render(request, f'base_app/contract_menu.html', context=context)
#
#
# def get_stock_store_by_group_id_contract(request, contract_slug):
#     _contract = Contracts.objects.get(filial__slug=filial_slug, slug=contract_slug)
#     group_id = _contract.id_groups_goods
#     if contract_slug == 'ok':
#         _df_res = query_goods_stock_by_group_id_ok(id_group_goods=group_id, _contract=_contract)
#     else:
#         _df_res = query_goods_stock_by_group_id(id_group_goods=group_id, _contract=_contract)
#     context['_df_res'] = _df_res
#     return render(request, f'base_app/contract_menu.html', context=context)


class Login(LoginView):
    template_name = 'base_app/const/login.html'

    def get_success_url(self):
        return super(Login, self).get_success_url()


class NotFound(LoginView):
    template_name = 'base_app/const/not_groups.html'

    def get_success_url(self):
        return super(NotFound, self).get_success_url()


def logout_view(request):
    logout(request)
    return redirect('home')


# dict_function = {
#     'order_btn_load_btn': load_order,
#     'check_goods_pg_btn_load_btn':  check_all_goods_in_pg,
#     'check_goods_pg_btn_search_btn': check_one_goods_in_pg,
#     'stock_pg_btn_load_btn': get_stock_store_by_group_id_contract,
#     'stock_pg_btn_search_btn': 'stock_one_goods_in_pg',
#     'stock_wms_btn_load_btn': 'stock_all_goods_in_wms',
#     'stock_wms_btn_search_btn': 'stock_one_goods_in_wms'
# }


def __clear_context():
    for key in context.copy():
        if key != 'filial' and key != 'menus':
            del context[key]
