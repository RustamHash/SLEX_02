import pandas as pd
from base_app.utils import data_to_dict, save_to_xml, start_client

dic_log_return = {'Расход': 0, 'Приход': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}
dic_const = {'id_sklad': '17709369', 'id_client': '17709365', 'id_postav': '17709367', 'delivery_type': 2}

NUM_ART = 13
NUM_QTY = 14
NUM_CLIENT = [11, 1]


def start(file_name, contract):
    for i in dic_log_return:
        dic_log_return[i] = 0
    try:
        __load_file(_wb_file=file_name, contract=contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': f'{str(e)}'}, False


def __load_file(_wb_file, contract):
    __dict_order = {'type_order': [],
                    'DeliveryDate': [],
                    'SalesId': [],
                    'Comment': [],
                    'Qty': [],
                    'ConsigneeAccount': [],
                    'Itemid': [],
                    }
    _df = pd.read_excel(_wb_file, header=None, dtype='object')
    _df.dropna(subset=_df.columns[1], inplace=True)
    _df.reset_index(drop=True, inplace=True)
    if 'Расходное' in _df.iloc[0, 1]:
        __parse_order(_df_order=_df, __dict_order=__dict_order, contract=contract)
    if 'Приходное' in _df.iloc[0, 1]:
        __parse_porder(_df_porder=_df, __dict_order=__dict_order, contract=contract)


def __parse_porder(_df_porder, __dict_order, contract):
    dic_const['type_order'] = 'Приход'
    dic_const['DeliveryDate'] = _df_porder.iloc[2, 3]
    dic_const['SalesId'] = _df_porder.iloc[3, 3]
    dic_const['Comment'] = _df_porder.iloc[3, 3]

    _df_porder.dropna(subset=_df_porder.columns[2], inplace=True)
    _df_porder.reset_index(drop=True, inplace=True)

    for index, row in _df_porder.iloc[1:30, :].iterrows():
        __dict_order['type_order'].append(dic_const['type_order'])
        __dict_order['DeliveryDate'].append(dic_const['DeliveryDate'])
        __dict_order['SalesId'].append(dic_const['SalesId'])
        __dict_order['Comment'].append(dic_const['Comment'])
        __dict_order['Itemid'].append(_df_porder.iloc[index, 2])
        __dict_order['Qty'].append(_df_porder.iloc[index, 4])
    __create_porder_data(__dict_order, contract)


def __parse_order(_df_order, __dict_order, contract):
    dic_const['type_order'] = 'Расход'
    dic_client = {
        'CustVendID': [],
        'CustVendName': [],
        'INN': [],
        'FactAddress': []
    }
    dic_const['DeliveryDate'] = _df_order.iloc[6, 3]
    dic_const['SalesId'] = _df_order.iloc[1, 3]
    dic_const['Comment'] = _df_order.iloc[1, 3]
    dic_const['ConsigneeAccount'] = _df_order.iloc[4, 6]
    dic_client['CustVendID'].append(_df_order.iloc[4, 6])
    dic_client['CustVendName'].append(_df_order.iloc[4, 3])
    dic_client['INN'].append(_df_order.iloc[3, 3])
    if str(_df_order.iloc[5, 3]) == 'nan':
        dic_client['FactAddress'] = 'Ростов-на-Дону, ул.1-я Луговая, 12'
    else:
        dic_client['FactAddress'] = str(_df_order.iloc[5, 3])
    __create_client_data(dic_client, contract)
    _df_order.dropna(subset=_df_order.columns[2], inplace=True)
    _df_order.reset_index(drop=True, inplace=True)
    for index, row in _df_order.iloc[1:30, :].iterrows():
        __dict_order['type_order'].append(dic_const['type_order'])
        __dict_order['DeliveryDate'].append(dic_const['DeliveryDate'])
        __dict_order['SalesId'].append(dic_const['SalesId'])
        __dict_order['Comment'].append(dic_const['Comment'])
        __dict_order['Itemid'].append(_df_order.iloc[index, 2])
        __dict_order['Qty'].append(_df_order.iloc[index, 4])
        __dict_order['ConsigneeAccount'].append(dic_const['ConsigneeAccount'])
    __create_order_data(__dict_order=__dict_order, _contract=contract)


def __create_order_data(__dict_order, _contract):
    df_order = pd.DataFrame()
    df_order['Itemid'] = __dict_order['Itemid']
    df_order['Qty'] = __dict_order['Qty']
    df_order['SalesId'] = __dict_order['SalesId']
    df_order['InventLocationId'] = dic_const['id_sklad']
    df_order['ConsigneeAccount'] = __dict_order['ConsigneeAccount']
    df_order['DeliveryDate'] = __dict_order['DeliveryDate']
    df_order['ManDate'] = ''
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = dic_const['delivery_type']
    df_order['Redelivery'] = 1
    df_order['OrderType'] = 1
    df_order['Comment'] = __dict_order['Comment']
    dic_order = data_to_dict(df_order)
    save_to_xml(data=dic_order, type_order='CustPicking', contract=_contract)
    dic_log_return['Расход'] += len(dic_order)


def __create_porder_data(__dict_order, _contract):
    df_porder = pd.DataFrame()
    df_porder['Itemid'] = __dict_order['Itemid']
    df_porder['Qty'] = __dict_order['Qty']
    df_porder['PurchId'] = __dict_order['SalesId']
    df_porder['VendAccount'] = dic_const['id_postav']
    df_porder['DeliveryDate'] = __dict_order['DeliveryDate']
    df_porder['InventLocationId'] = dic_const['id_sklad']
    df_porder['ProductionDate'] = '01-01-2024'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 1
    dic_porder = data_to_dict(df_porder)
    save_to_xml(data=dic_porder, type_order='VendReceipt', contract=_contract)
    dic_log_return['Приход'] += len(dic_porder)


def __create_client_data(__dict_client, _contract):
    df_client = pd.DataFrame()
    df_client['CustVendID'] = __dict_client['CustVendID']
    df_client['CustVendName'] = __dict_client['CustVendName']
    df_client['Phone'] = 1
    df_client['INN'] = __dict_client['INN']
    df_client['OKPO'] = 1
    df_client['KPP'] = 1
    df_client['FactAddress'] = __dict_client['FactAddress']
    dic_client = data_to_dict(df_client)
    save_to_xml(data=dic_client, type_order='CustVendTable', contract=_contract)
    dic_log_return['Справочник клиентов'] += len(dic_client)
