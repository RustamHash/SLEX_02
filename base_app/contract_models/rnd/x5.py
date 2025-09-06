import pandas as pd
from base_app.utils import data_to_dict, save_to_xml

dic_log_return = {'Расход': 0, 'Приход': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}


NUM_ORDER = 0
NUM_QTY_PRODUCT = 1
NUM_ART_PRODUCT = 0
NUM_NAME_PRODUCT = 10
NUM_DATE = 5
NUM_CLIENT = 18
NUM_COMMENT = 16

p_NUM_ORDER = 2
p_NUM_QTY_PRODUCT = 3
p_NUM_ART_PRODUCT = 2
p_NUM_NAME_PRODUCT = 26
p_NUM_DATE = 9
p_NUM_CLIENT = 25
p_NUM_COMMENT = 19

def start(file_name, contract=None):
    try:
        for i in dic_log_return:
            dic_log_return[i] = 0
        _df_order, _df_porder = __load_parse_file(file_name)
        if len(_df_order) > 0:
            __create_order(_df_order, contract)
        if len(_df_porder) > 0:
            __create_porder(_df_porder, contract)
            __create_product(_df_porder, contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def __load_parse_file(_wb_file):
    _df_order = pd.read_excel(_wb_file, dtype=object, sheet_name='Заказы на Выход')
    _df_porder = pd.read_excel(_wb_file, dtype=object, sheet_name='Заказы на вход')
    _df_order.dropna(subset=_df_order.columns[NUM_ORDER], inplace=True)
    _df_order.reset_index(drop=True, inplace=True)
    _df_porder.dropna(subset=_df_porder.columns[NUM_ORDER], inplace=True)
    _df_porder.reset_index(drop=True, inplace=True)
    return _df_order, _df_porder


def __create_order(_df, contract):
    df_order = pd.DataFrame()
    df_order['Itemid'] = _df[_df.columns[p_NUM_ART_PRODUCT]]
    df_order['Qty'] = _df[_df.columns[p_NUM_QTY_PRODUCT]]
    df_order['SalesId'] = _df[_df.columns[p_NUM_ORDER]]
    df_order['InventLocationId'] = contract.id_sklad
    df_order['ConsigneeAccount'] = _df[_df.columns[p_NUM_CLIENT]]
    df_order['DeliveryDate'] = _df[_df.columns[p_NUM_DATE]]
    df_order['ManDate'] = ''
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = 2
    df_order['Redelivery'] = 1
    df_order['OrderType'] = 1
    df_order['Comment'] = _df[_df.columns[p_NUM_COMMENT]]
    dic_order = data_to_dict(df_order)
    save_to_xml(dic_order, 'CustPicking', contract=contract)
    dic_log_return['Расход'] += len(dic_order)


def __create_porder(_df, contract):
    df_porder = pd.DataFrame()
    df_porder['Itemid'] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_porder['Qty'] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_porder['PurchId'] = _df[_df.columns[NUM_ORDER]]
    df_porder['VendAccount'] = contract.id_postav
    df_porder['DeliveryDate'] = _df[_df.columns[NUM_DATE]]
    df_porder['InventLocationId'] = contract.id_sklad
    df_porder['ProductionDate'] = '01.01.2023'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 0
    dic_order = data_to_dict(df_porder)
    save_to_xml(dic_order, 'VendReceipt', contract=contract)
    dic_log_return['Приход'] += len(dic_order)


def __create_product(_df, contract):
    bar_code_list = _df[_df.columns[0]]
    df_product = pd.DataFrame()
    df_product['ItemId'] = _df[_df.columns[0]]
    df_product['ItemName'] = _df[_df.columns[10]]
    df_product['NetWeight'] = _df[_df.columns[2]]
    df_product['NetWeightBox'] = _df[_df.columns[2]]
    df_product['NetWeightPack'] = _df[_df.columns[2]]
    df_product['BruttoWeight'] = _df[_df.columns[2]]
    df_product['BruttoWeightBox'] = _df[_df.columns[2]]
    df_product['BruttoWeightPack'] = _df[_df.columns[2]]
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
    df_product['EanBarcode'] = bar_code_list
    df_product['EanBarcodeBox'] = bar_code_list
    df_product['EanBarcodePack'] = bar_code_list
    df_product['Gs1Barcode'] = bar_code_list
    df_product['Gs1BarcodeBox'] = bar_code_list
    df_product['Gs1BarcodePack'] = bar_code_list
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, 'InventTable', contract=contract)
    dic_log_return['Справочник товаров'] += len(dic_product)