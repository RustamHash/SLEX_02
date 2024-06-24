import pandas as pd
from base_app.utils import data_to_dict, save_to_xml

dic_log_return = {'Расход': 0, 'Приход': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}
dic_const = {'id_sklad': '16718593', 'id_client': '16718603', 'id_postav': '16718594', 'delivery_type': 2}

NUM_DATE = 0
NUM_TYPE = 1
NUM_ORDER = 2
NUM_ART_PRODUCT = 3
NUM_NAME_PRODUCT = 4
NUM_QTY_PRODUCT = 5
NUM_COMMENT = 6


def start(file_name, contract):
    try:
        for i in dic_log_return:
            dic_log_return[i] = 0
        _df_order, _df_porder = __load_parse_file(file_name)
        if len(_df_order) > 0:
            __create_order(_df_order, contract)
        if len(_df_porder) > 0:
            __create_porder(_df_porder, contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype=object)
    _df_order = _df[_df['ВидНакладной'] == 'Расход'].copy()
    _df_porder = _df[_df['ВидНакладной'] == 'Приход'].copy()
    return _df_order, _df_porder


def __create_order(_df, contract):
    df_order = pd.DataFrame()
    df_order['Itemid'] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_order['Qty'] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_order['SalesId'] = _df[_df.columns[NUM_ORDER]]
    df_order['InventLocationId'] = dic_const['id_sklad']
    df_order['ConsigneeAccount'] = dic_const['id_client']
    df_order['DeliveryDate'] = _df[_df.columns[NUM_DATE]]
    df_order['ManDate'] = ''
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = dic_const['delivery_type']
    df_order['Redelivery'] = 1
    df_order['OrderType'] = 1
    df_order['Comment'] = _df[_df.columns[NUM_COMMENT]]
    dic_order = data_to_dict(df_order)
    save_to_xml(dic_order, 'CustPicking', contract=contract)
    dic_log_return['Расход'] += len(dic_order)


def __create_porder(_df, contract):
    df_porder = pd.DataFrame()
    df_porder['Itemid'] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_porder['Qty'] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_porder['PurchId'] = _df[_df.columns[NUM_ORDER]]
    df_porder['VendAccount'] = dic_const['id_postav']
    df_porder['DeliveryDate'] = _df[_df.columns[NUM_DATE]]
    df_porder['InventLocationId'] = dic_const['id_sklad']
    df_porder['ProductionDate'] = '01.01.2023'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 0
    dic_order = data_to_dict(df_porder)
    save_to_xml(dic_order, 'VendReceipt', contract=contract)
    dic_log_return['Приход'] += len(dic_order)
