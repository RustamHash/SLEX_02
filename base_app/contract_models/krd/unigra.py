import pandas as pd
from base_app.utils import data_to_dict, save_to_xml

dic_log_return = {'Расход': 0, 'Приход': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}
# dic_const = {'id_sklad': '16721418', 'id_client': '16721420', 'id_postav': '16721417', 'delivery_type': 2}

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
            # _df_porder[_df_porder.columns[NUM_ART_PRODUCT]] = _df_porder[_df_porder.columns[NUM_ART_PRODUCT]].apply(
            #     __create_prefix)
            # print(_df_porder.to_markdown())
            __create_porder(_df_porder, contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def add_goods(file_name, contract):
    try:
        for i in dic_log_return:
            dic_log_return[i] = 0
        _df_ka = __get_df_goods(_file_name=file_name)
        __create_product(_df=_df_ka, contract=contract)
        return dic_log_return, False
    except Exception as e:
        return {'error': str(e)}, True


def __get_df_goods(_file_name):
    _df_new = pd.read_excel(_file_name)
    # df = _df_new.dropna(subset=[_df_new.columns[1]])
    _df_new.reset_index(drop=True, inplace=True)
    return _df_new


def __create_prefix(_data):
    prefix = "uni"
    _data = f'{prefix}{_data}'
    return _data


def __create_prefix_num_order(_data):
    prefix = "uni"
    _data = f'{prefix}_{_data}'
    return _data


def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype=object)
    _df[_df.columns[NUM_ORDER]] = _df[_df.columns[NUM_ORDER]].apply(__create_prefix_num_order)
    _df_order = _df[_df['ВидНакладной'] == 'Расход'].copy()
    _df_porder = _df[_df['ВидНакладной'] == 'Приход'].copy()
    return _df_order, _df_porder


def __create_order(_df, contract):
    df_order = pd.DataFrame()
    df_order['Itemid'] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_order['Qty'] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_order['SalesId'] = _df[_df.columns[NUM_ORDER]]
    df_order['InventLocationId'] = contract.id_sklad
    df_order['ConsigneeAccount'] = contract.id_client
    df_order['DeliveryDate'] = _df[_df.columns[NUM_DATE]]
    df_order['ManDate'] = ''
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = contract.delivery_type
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
    df_porder['VendAccount'] = contract.id_postav
    df_porder['DeliveryDate'] = _df[_df.columns[NUM_DATE]]
    df_porder['InventLocationId'] = contract.id_sklad
    df_porder['ProductionDate'] = '01.01.2023'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 0
    df_porder['Comment'] = _df[_df.columns[NUM_COMMENT]]
    dic_order = data_to_dict(df_porder)
    save_to_xml(dic_order, 'VendReceipt', contract=contract)
    dic_log_return['Приход'] += len(dic_order)


dic_columns = {0: 'Артикул', 1: 'Наименование', 2: 'Штрих-код упаковки', 3: 'Штрих-код блока', 4: 'Штрих-код короба',
               5: 'Вес нетто шт', 6: 'Вес брутто шт', 7: 'Штук в коробе', 8: 'Штук в блоке',
               9: 'Штук на палете', 10: 'Коробов на палете', 11: 'Коробов в слое',
               12: 'Длина шт в мм', 13: 'Ширина шт в мм', 14: 'Высота шт в мм', 15: 'Обьем шт в м3',
               16: 'Срок годности в днях', 17: 'Цена за шт'}


def __create_product(_df, contract):
    df_product = pd.DataFrame()
    df_product['ItemId'] = _df[dic_columns[0]]
    df_product['ItemName'] = _df[dic_columns[1]]
    df_product['NetWeight'] = _df[dic_columns[6]]
    df_product['NetWeightBox'] = _df[dic_columns[6]]
    df_product['NetWeightPack'] = _df[dic_columns[6]]
    df_product['BruttoWeight'] = _df[dic_columns[6]]
    df_product['BruttoWeightBox'] = _df[dic_columns[6]]
    df_product['BruttoWeightPack'] = _df[dic_columns[6]]
    df_product['Quantity'] = _df[dic_columns[7]]
    df_product['standardShowBoxQuantity'] = 1
    df_product['UnitId'] = 'шт'
    df_product['Depth'] = _df[dic_columns[12]]
    df_product['Height'] = _df[dic_columns[14]]
    df_product['Width'] = _df[dic_columns[13]]
    df_product['BoxDepth'] = _df[dic_columns[12]]
    df_product['BoxHeight'] = _df[dic_columns[14]]
    df_product['BoxWidth'] = _df[dic_columns[13]]
    df_product['BlockDepth'] = _df[dic_columns[12]]
    df_product['BlockHeight'] = _df[dic_columns[14]]
    df_product['BlockWidth'] = _df[dic_columns[13]]
    df_product['StandardPalletQuantity'] = _df[dic_columns[9]]
    df_product['QtyPerLayer'] = 1
    df_product['Price'] = _df[dic_columns[17]]
    df_product['ShelfLife'] = _df[dic_columns[16]]
    df_product['EanBarcode'] = _df[dic_columns[2]]
    df_product['EanBarcodeBox'] = _df[dic_columns[4]]
    df_product['EanBarcodePack'] = _df[dic_columns[4]]
    df_product['Gs1Barcode'] = _df[dic_columns[2]]
    df_product['Gs1BarcodeBox'] = _df[dic_columns[4]]
    df_product['Gs1BarcodePack'] = _df[dic_columns[4]]
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, 'InventTable', contract=contract)
    dic_log_return['Справочник товаров'] += len(dic_product)
