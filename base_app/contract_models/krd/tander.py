import pandas as pd
from base_app.utils import data_to_dict, save_to_xml

dic_log_return = {'Расход': 0, 'Приход': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}
dic_const = {'id_sklad': 231100, 'id_client': '16718603', 'id_postav': '16713163', 'delivery_type': 2}

ADD_PALLET = False

NUM_DATE = 56
NUM_ORDER = 0
NUM_ART_PRODUCT = 3
NUM_NAME_PRODUCT = 4
NUM_QTY_PRODUCT = 6
NUM_CLIENT = 13
NUM_POSTAV = 11
NUM_COMMENT = 0
NUM_MAN_DATE = 18
NUM_QTY_PALLET = 7

NUM_DeliveryDate = 6
NUM_PurchId = 0
NUM_Itemid = 2
NUM_Qty = 7
NUM_VendAccount = 4
NUM_Comment = 0


def start(file_name, contract):
    # __df_product = pd.read_excel(file_name, dtype=object)
    # __create_product(__df_product, contract)
    # return dic_log_return, True
    try:
        for i in dic_log_return:
            dic_log_return[i] = 0
        _df_order, _df_porder, _ka = __load_parse_file(file_name)
        if _ka:
            if len(_df_porder) > 0:
                __create_porder_ka(_df_porder, contract)
        else:
            if len(_df_order) > 0:
                __create_order(_df_order, contract)
            if len(_df_porder) > 0:
                __create_porder(_df_porder, contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype=object)
    _df_order, _df_porder = pd.DataFrame(), pd.DataFrame()
    _ka = False
    if str(_wb_file).lower().find("вс") > 0 or str(_wb_file).lower().find("отгрузок") > 0:
        _df['Код РЦ Отправителя'] = _df['Код РЦ Отправителя'].astype(int)
        _df['Код РЦ Получателя'] = _df['Код РЦ Получателя'].astype(str)
        _df_order = _df[_df['Код РЦ Отправителя'] == dic_const['id_sklad']].copy()
        _df_porder = _df[_df['Код РЦ Получателя'] == dic_const['id_sklad']].copy()
    else:
        _df_porder = _df.copy()
        _ka = True
    return _df_order, _df_porder, _ka


def __add_pallet(__dict):
    i = 0
    for key in __dict.keys():
        print(i + 1)
        _ = __dict[key][0].copy()
        _['Itemid'] = 1038000001
        _['Qty'] = 33
        __dict[key][len(__dict[key]) + 1] = _
    return __dict


def __create_order(_df, contract):
    df_order = pd.DataFrame()
    df_order['Itemid'] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_order['Qty'] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_order['SalesId'] = _df[_df.columns[NUM_ORDER]]
    df_order['InventLocationId'] = dic_const['id_sklad']
    df_order['ConsigneeAccount'] = _df[_df.columns[NUM_CLIENT]].apply(lambda x: f'tnd{x}')
    df_order['DeliveryDate'] = _df[_df.columns[NUM_DATE]]
    df_order['ManDate'] = _df[_df.columns[NUM_MAN_DATE]]
    df_order['ManDate'] = df_order['ManDate'].fillna(_df[_df.columns[NUM_DATE]])
    df_order['SalesUnit'] = 'шт'
    df_order['Delivery'] = dic_const['delivery_type']
    df_order['Redelivery'] = 1
    df_order['OrderType'] = 1
    df_order['Comment'] = _df[_df.columns[NUM_COMMENT]]
    dic_order = data_to_dict(df_order)
    if ADD_PALLET:
        dic_order = __add_pallet(dic_order)
    save_to_xml(dic_order, 'CustPicking', contract=contract)
    dic_log_return['Расход'] += len(dic_order)


def __create_porder(_df, contract):
    df_porder = pd.DataFrame()
    df_porder['Itemid'] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_porder['Qty'] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_porder['PurchId'] = _df[_df.columns[NUM_ORDER]]
    df_porder['VendAccount'] = _df[_df.columns[NUM_POSTAV]]
    df_porder['DeliveryDate'] = _df[_df.columns[NUM_DATE]]
    df_porder['InventLocationId'] = dic_const['id_sklad']
    df_porder['ProductionDate'] = '01.01.2023'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = _df[_df.columns[NUM_ORDER]]
    df_porder['Price'] = 0
    df_porder['Comment'] = _df[_df.columns[NUM_COMMENT]]
    dic_order = data_to_dict(df_porder)
    if ADD_PALLET:
        dic_order = __add_pallet(dic_order)
    save_to_xml(dic_order, 'VendReceipt', contract=contract)
    dic_log_return['Приход'] += len(dic_order)


def __create_porder_ka(_df, contract):
    df_porder = pd.DataFrame()
    df_porder['Itemid'] = _df[_df.columns[NUM_Itemid]]
    df_porder['Qty'] = _df[_df.columns[NUM_Qty]]
    df_porder['PurchId'] = _df[_df.columns[NUM_PurchId]]
    df_porder['VendAccount'] = _df[_df.columns[NUM_VendAccount]]
    df_porder['DeliveryDate'] = _df[_df.columns[NUM_DeliveryDate]]
    df_porder['InventLocationId'] = dic_const['id_sklad']
    df_porder['ProductionDate'] = '01.01.2024'
    df_porder['PurchUnit'] = 'шт'
    df_porder['PurchTTN'] = 1
    df_porder['Price'] = 0
    df_porder['Comment'] = _df[_df.columns[NUM_Comment]]
    dic_order = data_to_dict(df_porder)
    if ADD_PALLET:
        dic_order = __add_pallet(dic_order)
    save_to_xml(dic_order, 'VendReceipt', contract=contract)
    dic_log_return['Приход'] += len(dic_order)


def star_client(file_name, contract):
    _df = pd.read_excel(file_name)
    _df.fillna(1, inplace=True)
    df_client = pd.DataFrame()
    df_client['CustVendID'] = _df[_df.columns[0]]
    df_client['CustVendName'] = _df[_df.columns[1]]
    df_client['Phone'] = _df[_df.columns[4]]
    df_client['INN'] = _df[_df.columns[2]].astype(int)
    df_client['OKPO'] = 1
    df_client['KPP'] = _df[_df.columns[5]].astype(int)
    df_client['FactAddress'] = _df[_df.columns[3]]
    dic_client = data_to_dict(df_client)
    save_to_xml(dic_client, 'CustVendTable', contract=contract)
    dic_log_return['Справочник клиентов'] += len(dic_client)


def __create_product(_df, contract):
    df_product = pd.DataFrame()
    df_product['ItemId'] = _df[_df.columns[0]]
    df_product['ItemName'] = _df[_df.columns[1]].astype(str)
    df_product['NetWeight'] = _df[_df.columns[5]]
    df_product['NetWeightBox'] = 500
    df_product['NetWeightPack'] = 500
    df_product['BruttoWeight'] = _df[_df.columns[5]]
    df_product['BruttoWeightBox'] = 500
    df_product['BruttoWeightPack'] = 500
    df_product['Quantity'] = _df[_df.columns[7]]
    df_product['standardShowBoxQuantity'] = 1
    df_product['UnitId'] = 'шт'
    df_product['Depth'] = _df[_df.columns[13]]
    df_product['Height'] = _df[_df.columns[15]]
    df_product['Width'] = _df[_df.columns[14]]
    df_product['BoxDepth'] = 0
    df_product['BoxHeight'] = 0
    df_product['BoxWidth'] = 0
    df_product['BlockDepth'] = 0
    df_product['BlockHeight'] = 0
    df_product['BlockWidth'] = 0
    df_product['StandardPalletQuantity'] = _df[_df.columns[11]]
    df_product['QtyPerLayer'] = 1
    df_product['Price'] = _df[_df.columns[18]]
    df_product['ShelfLife'] = _df[_df.columns[17]]
    df_product['EanBarcode'] = _df[_df.columns[2]]
    df_product['EanBarcodeBox'] = _df[_df.columns[4]]
    df_product['EanBarcodePack'] = _df[_df.columns[4]]
    df_product['Gs1Barcode'] = 0
    df_product['Gs1BarcodeBox'] = 0
    df_product['Gs1BarcodePack'] = 0
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, 'InventTable', contract=contract)
    dic_log_return['Справочник товаров'] += len(dic_product)
