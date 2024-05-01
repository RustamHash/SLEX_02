from django.urls import reverse_lazy

import pandas as pd

from pprint import pprint
from pg_sql.models import PgStocks, PgGoods

from base_app.contract_models import neo_stroy_krd
from base_app.contract_models.krd import toshev, kzvs, agro
from base_app.contract_models.rnd import ok
from base_app.contract_models.vlg import *

dict_module = {
    'toshev-rf': toshev,
    'kzvs': kzvs,
    'neo-stroy-krd': neo_stroy_krd,
    'neo-stroy-sochi': neo_stroy_krd,
    'agrokompleks': agro,
}


# dict_function_contract = {
#     # 'order_btn_load_btn': load_order,
#     'check_goods_pg_btn_load_btn': get_goods_list_by_marking_goods,
#     'check_goods_pg_btn_load_btn': PgGoods().get_goods_list_by_marking_goods()
#     'check_goods_pg_btn_search_btn': get_good_by_marking_goods,
#     'stock_pg_btn_load_btn': query_goods_stock_by_group_id,
#     'stock_pg_btn_search_btn': query_goods_stock_by_group_id_ok,
#     'stock_wms_btn_load_btn': 'stock_all_goods_in_wms',
#     'stock_wms_btn_search_btn': 'stock_one_goods_in_wms'
# }

def normalizing_of_start_function(_data):
    __msg_error = f''
    __error_valid = False
    __context = _data.get('context', False)
    __operation = __context.get('operation', False)
    __operation_btn = __context.get('operation_btn', False)
    __contract = _data.get('contract', False)
    __filial = _data.get('filial_slug', False)
    __request = _data.get('request', False)
    __file = __request.FILES.get('file', False)
    __marking = __request.POST.get('search_input', False)
    __function_name = f'{__operation}_{__operation_btn}'
    if __function_name == 'order_btn_load_btn':
        if dict_module.get(__contract.slug, False):
            try:
                __result, __error_valid = dict_module[__contract.slug].start(__file, __contract)
                print(f'__result: {__result}')
                if __error_valid:
                    return __result, __error_valid
            except Exception as e:
                __error_valid = True
                __msg_error += f'\n{e}'
                return __msg_error, __error_valid
        else:
            __error_valid = True
            __msg_error += (f'\nДля данного контракта эта функция еще не настроена!'
                            f'\nОбратитесь к разработчику!')
            return __msg_error, __error_valid
    print(f'_function_name: {__function_name}')

    __msg_error += f'\n__operation: {__operation_btn}'
    __msg_error += f'\n__file: {__file}'
    return __msg_error, __error_valid
    # print(f'__context: {__context}')
    # print(f'__operation: {__operation}')
    # print(f'__operation_btn: {__operation_btn}')
    # print(f'__contract: {__contract}')
    # print(f'__filial: {__filial}')
    # print(f'__request: {__request}')
    # print(f'__file: {__file}')
