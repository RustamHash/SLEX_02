import pandas as pd
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect

from base_app.models import Filial, Contracts, Menu, Operations, Reports
from base_app.utils import comparison_stock
from base_app.contract_models import neo_stroy_krd

from base_app.contract_models.rnd import ok

from base_app.contract_models.krd import toshev, kzvs, agro, soiprom

from pg_sql.models import PgStocks, PgGoods
from wms_app.models import WmsStocks, WmsGoods

context = {}
dict_module = {
    'toshev-rf': toshev,
    'kzvs': kzvs,
    'neo-stroy-krd': neo_stroy_krd,
    'neo-stroj-sochi': neo_stroy_krd,
    'agrokompleks': agro,
    'neo-stroj-rostov': neo_stroy_krd,
    'ok': ok,
    'soiprom': soiprom
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
    # context['operations'] = Operations.objects.filter(as_active=True, contract__slug=kwargs['_contract_slug'])

    context['contract'] = Contracts.objects.get(filial__slug=context['filial'].slug, slug=kwargs['_contract_slug'])
    context['operations'] = context['contract'].operations.filter(as_active=True)
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

    if kwargs['_operation_slug'] == 'build_peresort':
        _file = request.FILES['file']
        print(_file)
        context['result'] = ok.build_peresort(_file_name=_file, _contract=context['contract'])
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
    if kwargs['_operation_slug'] == 'comparison-stock':
        __file_pg_stock = PgStocks().query_goods_stock_by_group_id(_contract=context['contract'])
        __file_wms_stock = WmsStocks().get_goods_by_guid_group(_contract=context['contract'])
        context['result'] = comparison_stock(_contract=context['contract'], __file_pg_stock=__file_pg_stock,
                                             __file_wms_stock=__file_wms_stock)
        try:
            return FileResponse(open(context['result'], 'rb'))
        except Exception as e:
            context['result'] = {'error': e}
            return render(request, f'base_app/show_result.html', context=context)

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
            context['result'] = WmsStocks().get_goods_by_guid_group(_contract=context['contract'])
        try:
            return FileResponse(open(context['result'], 'rb'))
        except Exception as e:
            context['result'] = {'error': e}
            return render(request, f'base_app/show_result.html', context=context)
    return render(request, f'base_app/operations.html', context=context)


def show_reports(request, **kwargs):
    reports = context['filial'].reports.filter(as_active=True)
    context['reports'] = reports
    return render(request, f'base_app/reports.html', context=context)


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


def __clear_context():
    for key in context.copy():
        if key != 'filial' and key != 'menus':
            del context[key]
