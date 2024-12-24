# -*- coding: utf-8 -*-
# base_app\contract_models\neo_stroy_krd.py
import pandas as pd
import datetime

from base_app.utils import data_to_dict, save_to_xml

dic_log_return = {'Расход': 0, 'Приход': 0, 'Доступы': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}
dic_const = {}
dic_const_krd = {'id_sklad': '16718318', 'id_client': '16718173', 'id_postav': '16718148', 'delivery_type': 2,
                 'id_engineer': '16720118'}
dic_const_sochi = {'id_sklad': '16718149', 'id_client': '16718173', 'id_postav': '16718148', 'delivery_type': 2,
                   'id_engineer': '16720118'}
dic_const_rnd = {'id_sklad': '17017234', 'id_client': '17017253', 'id_postav': '17017238', 'delivery_type': 2,
                 'id_engineer': '17011254'}
NUM_QTY_ORDER = 50
NUM_QTY_PORDER = 51
NUM_QTY_ENGINEER = 52


def start(file_name, contract):
    global dic_const, dic_const_sochi, dic_const_krd, dic_const_rnd
    if contract.slug == 'neo-stroj-sochi':
        dic_const = dic_const_sochi
    elif contract.slug == 'neo-stroj-rostov':
        dic_const = dic_const_rnd
    else:
        dic_const = dic_const_krd
    try:
        for key, value in dic_log_return.items():
            dic_log_return[key] = 0
        _df_order, _df_porder, _df_engineer = __load_parse_file(file_name)
        if len(_df_order) > 0:
            __create_order(_df_order, contract, engineer=False)
        if len(_df_porder) > 0:
            __create_porder(_df_porder, contract, engineer=False)
            __create_product(_df_porder, contract)
        if len(_df_engineer) > 0:
            __create_order(_df_engineer, contract, engineer=True)
            __create_porder(_df_engineer, contract, engineer=True)
        if len(_df_order) == 0 and len(_df_porder) == 0 and len(_df_engineer) == 0:
            return {'Ошибка \n'
                    'Должно быть заполненно одно из полей:\n'
                    '6.2. Приемка УС на складе\n'
                    '6.3. Отгрузка УС со склада\n'
                    '6.4. Перемещение УС на складе\n': 1}, False
        dic_log_return['Доступы'] = int(dic_log_return['Доступы'] / 2)
        return dic_log_return, False
    except Exception as e:
        return {'error': str(e)}, True


def __load_parse_file(_wb_file):
    pd.set_option('future.no_silent_downcasting', True)
    _df = pd.read_excel(_wb_file)
    _df.drop(index=[0], inplace=True)
    _df.dropna(subset=_df.columns[1], inplace=True)
    _df.reset_index(drop=True, inplace=True)
    dt = __create_datetime()
    _df[_df.columns[6]] = _df[_df.columns[6]].astype(str).str.replace('\'', '')
    _df[_df.columns[5]] = _df[_df.columns[5]].astype(str).str.replace('\'', '')
    _df[_df.columns[1]] = _df[_df.columns[1]].astype(str).str.replace('б/н', dt)
    _df[_df.columns[1]] = _df[_df.columns[1]].astype(str).str.replace(r'б\н', dt)
    _df = _df.fillna(0)
    _df[_df.columns[51]] = _df[_df.columns[51]].astype(int)
    _df[_df.columns[50]] = _df[_df.columns[50]].astype(int)
    _df[_df.columns[52]] = _df[_df.columns[52]].astype(int)
    _df_order = _df[_df[_df.columns[51]] > 0].copy()
    _df_porder = _df[_df[_df.columns[50]] > 0].copy()
    _df_engineer = _df[_df[_df.columns[52]] > 0].copy()
    return _df_order, _df_porder, _df_engineer


def __create_datetime():
    _dt = datetime.datetime.now() + datetime.timedelta(days=1)
    _dt = _dt.strftime("%Y%m%d-%H%M%S")
    _dt = str(_dt)
    return _dt


def __create_datetime_order():
    _dt = datetime.datetime.now() + datetime.timedelta(days=1)
    _dt = _dt.strftime("%Y-%m-%d")
    return _dt


def __create_order(_df, contract, engineer):
    df_order = pd.DataFrame()
    df_order['SalesId'] = _df[_df.columns[1]]
    df_order['InventLocationId'] = dic_const['id_sklad']
    if engineer:
        df_order['ConsigneeAccount'] = dic_const['id_engineer']
    else:
        df_order['ConsigneeAccount'] = dic_const['id_client']
    df_order['DeliveryDate'] = __create_datetime_order()
    df_order['ManDate'] = __create_datetime_order()
    df_order['Itemid'] = _df[_df.columns[6]]
    if engineer:
        df_order['Qty'] = _df[_df.columns[52]]
    else:
        df_order['Qty'] = _df[_df.columns[51]]
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = dic_const['delivery_type']
    df_order['Redelivery'] = 1
    df_order['OrderType'] = 1
    df_order['Comment'] = _df[_df.columns[11]]
    dic_order = data_to_dict(df_order)
    save_to_xml(dic_order, 'CustPicking', contract=contract)
    if engineer:
        dic_log_return['Доступы'] += len(dic_order)
    else:
        dic_log_return['Расход'] += len(dic_order)


def __create_porder(_df, contract, engineer):
    df_porder = pd.DataFrame()
    df_porder['Itemid'] = _df[_df.columns[6]]
    if engineer:
        df_porder['Qty'] = _df[_df.columns[52]]
    else:
        df_porder['Qty'] = _df[_df.columns[50]]
    df_porder['PurchId'] = _df[_df.columns[1]]
    if engineer:
        df_porder['VendAccount'] = dic_const['id_engineer']
    else:
        df_porder['VendAccount'] = dic_const['id_postav']
    df_porder['DeliveryDate'] = __create_datetime_order()
    df_porder['InventLocationId'] = dic_const['id_sklad']
    df_porder['ProductionDate'] = __create_datetime_order()
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 1
    df_porder['Comment'] = _df[_df.columns[1]]
    dic_porder = data_to_dict(df_porder)
    save_to_xml(dic_porder, 'VendReceipt', contract=contract)
    if engineer:
        dic_log_return['Доступы'] += len(dic_porder)
    else:
        dic_log_return['Приход'] += len(dic_porder)


def __create_product(_df, contract):
    df_product = pd.DataFrame()
    df_product['ItemId'] = _df[_df.columns[6]]
    df_product['ItemName'] = _df[_df.columns[5]].astype(str) + '_' + _df[_df.columns[7]].astype(str)
    df_product['NetWeight'] = 500
    df_product['NetWeightBox'] = 500
    df_product['NetWeightPack'] = 500
    df_product['BruttoWeight'] = 500
    df_product['BruttoWeightBox'] = 500
    df_product['BruttoWeightPack'] = 500
    df_product['Quantity'] = 1
    df_product['standardShowBoxQuantity'] = 1
    df_product['UnitId'] = 'шт'
    df_product['Depth'] = 1200
    df_product['Height'] = 1800
    df_product['Width'] = 800
    df_product['BoxDepth'] = 1200
    df_product['BoxHeight'] = 1800
    df_product['BoxWidth'] = 800
    df_product['BlockDepth'] = 1200
    df_product['BlockHeight'] = 1800
    df_product['BlockWidth'] = 800
    df_product['StandardPalletQuantity'] = 1
    df_product['QtyPerLayer'] = 1
    df_product['Price'] = 1
    df_product['ShelfLife'] = 1095
    df_product['EanBarcode'] = _df[_df.columns[5]]
    df_product['EanBarcodeBox'] = _df[_df.columns[5]]
    df_product['EanBarcodePack'] = _df[_df.columns[5]]
    df_product['Gs1Barcode'] = _df[_df.columns[5]]
    df_product['Gs1BarcodeBox'] = _df[_df.columns[5]]
    df_product['Gs1BarcodePack'] = _df[_df.columns[5]]
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, 'InventTable', contract=contract)
    dic_log_return['Справочник товаров'] += len(dic_product)
