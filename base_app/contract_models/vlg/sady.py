import pandas as pd
import numpy as np
from base_app.utils import data_to_dict, save_to_xml, generator_bar_code

dic_log_return = {'Расход': 0, 'Приход': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}
dic_const = {'id_sklad': '17708910', 'id_client': '17708908', 'id_postav': '17708906', 'delivery_type': 2}

NUM_DATE = 5
NUM_TYPE = 4
NUM_ORDER = 0
NUM_ART_PRODUCT = 6
NUM_NAME_PRODUCT = 1
NUM_QTY_PRODUCT = 3
NUM_COMMENT = 0
NUM_BAR_CODE_PAC = 7
NUM_BAR_CODE_UNIT = 8


def start(file_name, contract):
    try:
        for i in dic_log_return:
            dic_log_return[i] = 0
        _df_order, _df_porder = __specific_parse(file_name)
        if len(_df_order) > 0:
            __create_order(_df_order, contract)
        if len(_df_porder) > 0:
            _df_porder.to_excel('test.xlsx')
            __create_porder(_df_porder, contract)
            __create_product(_df_porder, contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def __update_columns_number(_df):
    global NUM_DATE, NUM_TYPE, NUM_ORDER, NUM_ART_PRODUCT, NUM_NAME_PRODUCT, NUM_QTY_PRODUCT, NUM_COMMENT, NUM_BAR_CODE_PAC, NUM_BAR_CODE_UNIT
    NUM_DATE = _df.columns.get_loc('Дата выгрузки')
    NUM_TYPE = _df.columns.get_loc('Склад выгрузки')
    NUM_ORDER = _df.columns.get_loc('Контейнер')
    NUM_ART_PRODUCT = _df.columns.get_loc('Код упаковки')
    NUM_NAME_PRODUCT = _df.columns.get_loc('Номенклатура')
    NUM_QTY_PRODUCT = _df.columns.get_loc('Количество')
    NUM_COMMENT = _df.columns.get_loc('Контейнер')
    NUM_BAR_CODE_PAC = _df.columns.get_loc('Штрихкод УП')
    NUM_BAR_CODE_UNIT = _df.columns.get_loc('Штрихкод ШТ')

def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype=object)
    _df_order = _df[_df['ВидНакладной'] == 'Расход'].copy()
    _df_porder = _df[_df['ВидНакладной'] == 'Приход'].copy()
    return _df_order, _df_porder


def __specific_parse(_wb_file):
    _df_new = pd.read_excel(_wb_file, dtype=object)
    _df_new[_df_new.columns[0]] = _df_new[_df_new.columns[0]].ffill()
    df = _df_new.dropna(subset=[_df_new.columns[1]])
    df.columns = df.iloc[0]
    df.rename(columns=lambda x: x.strip())
    df.drop(df.index[:1], inplace=True)
    df.reset_index(drop=True, inplace=True)
    __update_columns_number(_df=df)
    df[df.columns[NUM_ART_PRODUCT]] = df[df.columns[NUM_ART_PRODUCT]].str.replace("*", "")
    df[df.columns[NUM_BAR_CODE_UNIT]] = df[df.columns[NUM_BAR_CODE_UNIT]].replace(np.nan, 0)
    df[df.columns[NUM_BAR_CODE_PAC]] = df[df.columns[NUM_BAR_CODE_PAC]].replace(np.nan, 0)
    df[df.columns[NUM_QTY_PRODUCT]] = df[df.columns[NUM_QTY_PRODUCT]].astype(int)
    _df_porder = df[df[df.columns[NUM_TYPE]] == 'НЕО-ТРЕЙД'].copy()
    _df_order = df[df[df.columns[NUM_TYPE]] != 'НЕО-ТРЕЙД'].copy()
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


def __create_product(_df, contract):
    df_product = pd.DataFrame()
    df_product['ItemId'] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_product['ItemName'] = _df[_df.columns[NUM_NAME_PRODUCT]].astype(str)
    df_product['NetWeight'] = 0.100
    df_product['NetWeightBox'] = 0.100
    df_product['NetWeightPack'] = 0.100
    df_product['BruttoWeight'] = 0.100
    df_product['BruttoWeightBox'] = 0.100
    df_product['BruttoWeightPack'] = 0.100
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
    df_product['EanBarcode'] = _df[_df.columns[NUM_BAR_CODE_UNIT]]
    df_product['EanBarcodeBox'] = _df[_df.columns[NUM_BAR_CODE_PAC]]
    df_product['EanBarcodePack'] = _df[_df.columns[NUM_BAR_CODE_PAC]]
    df_product['Gs1Barcode'] = _df[_df.columns[NUM_BAR_CODE_UNIT]]
    df_product['Gs1BarcodeBox'] = _df[_df.columns[NUM_BAR_CODE_PAC]]
    df_product['Gs1BarcodePack'] = _df[_df.columns[NUM_BAR_CODE_PAC]]
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, 'InventTable', contract=contract)
    dic_log_return['Справочник товаров'] += len(dic_product)
