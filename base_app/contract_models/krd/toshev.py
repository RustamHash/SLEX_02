import os
import pandas as pd
from base_app.utils import data_to_dict, save_to_xml

dic_log_return = {'Расход': 0, 'Приход': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}
dic_const = {'id_sklad': '16714743', 'id_client': '16716869', 'id_postav': '16714742', 'delivery_type': 2}

NUM_ART = 13
NUM_QTY = 14
NUM_CLIENT = [11, 1]


def start(file_name, contract):
    print(file_name)
    print(contract)
    for i in dic_log_return:
        dic_log_return[i] = 0
    try:
        dic_const['num_order'] = __num_order_create(file_name.name)
        dic_const['date_order'] = __create_date()
        df = __load_parse_file(file_name)
        if 'НЕО-ТРЕЙД' in dic_const['comment']:
            __create_porder_data(_df=df, _contract=contract)
        else:
            __create_order_data(_df=df, _contract=contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype='object')
    dic_const['comment'] = __name_client_create(_df.iloc[11, 1])
    _df.dropna(subset=_df.columns[NUM_ART], inplace=True)
    _df.reset_index(drop=True, inplace=True)
    _df.drop(index=[0], inplace=True)
    _df.reset_index(drop=True, inplace=True)

    # Заполняем массив для заявки
    # df_order = pd.DataFrame()
    # df_order['Itemid'] = _df[_df.columns[NUM_ART]].copy()
    # df_order['Qty'] = _df[_df.columns[NUM_QTY]].copy()
    # if 'НЕО-ТРЕЙД' in _client:
    #     df_order['OrderType'] = 0
    #     df_order['PurchId'] = dic_const['num_order']
    #     df_order['PurchUnit'] = 'шт'
    # else:
    #     df_order['OrderType'] = 1
    #     df_order['SalesId'] = dic_const['num_order']
    #     df_order['SalesUnit'] = 'шт'
    # df_order['ConsigneeAccount'] = dic_const['id_client']
    # df_order['VendAccount'] = dic_const['id_postav']
    # df_order['InventLocationId'] = dic_const['id_sklad']
    # df_order['Delivery'] = dic_const['delivery_type']
    # df_order['Redelivery'] = 0.00
    # df_order['DeliveryDate'] = dic_const['date_order']
    # df_order['ManDate'] = dic_const['date_order']
    # df_order['Price'] = 1.00
    # df_order['UseEDO'] = 0
    # df_order['Comment'] = _client
    # df_order['PurchTTN'] = dic_const['num_order']
    return _df


def __create_order_data(_df, _contract):
    df_order = pd.DataFrame()
    df_order['Itemid'] = _df[_df.columns[NUM_ART]]
    df_order['Qty'] = _df[_df.columns[NUM_QTY]]
    df_order['SalesId'] = dic_const['num_order']
    df_order['InventLocationId'] = dic_const['id_sklad']
    df_order['ConsigneeAccount'] = dic_const['id_client']
    df_order['DeliveryDate'] = dic_const['date_order']
    df_order['ManDate'] = ''
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = dic_const['delivery_type']
    df_order['Redelivery'] = 1
    df_order['OrderType'] = 1
    df_order['Comment'] = dic_const['comment']
    dic_order = data_to_dict(df_order)
    save_to_xml(dic_order, 'CustPicking', contract=_contract)
    dic_log_return['Расход'] += len(dic_order)


def __create_porder_data(_df, _contract):
    df_porder = pd.DataFrame()
    df_porder['Itemid'] = _df[_df.columns[NUM_ART]]
    df_porder['Qty'] = _df[_df.columns[NUM_QTY]]
    df_porder['PurchId'] = dic_const['num_order']
    df_porder['VendAccount'] = dic_const['id_postav']
    df_porder['DeliveryDate'] = dic_const['date_order']
    df_porder['InventLocationId'] = dic_const['id_sklad']
    df_porder['ProductionDate'] = '01-01-2023'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 1
    dic_porder = data_to_dict(df_porder)
    save_to_xml(dic_porder, 'VendReceipt', _contract)
    dic_log_return['Приход'] += len(dic_porder)


def __name_client_create(s):
    n = s.find(':') + 2
    k = len(s)
    client = s[n:k]
    return client


def __create_date():
    import datetime
    _dt = datetime.datetime.now().date() + datetime.timedelta(days=1)
    return _dt


def __num_order_create(s):
    n = s.find('№') + 1
    k = s.find(' ', n)
    num = s[n:k]
    return num
