import warnings
import pandas as pd

from base_app.utils import __save_reports_stock_to_excel, save_to_xml, data_to_dict
from wms_app.models import WmsStocks

col_art_num = 'Номенклатура.Артикул'
col_name_num = 'Номенклатура.Description'
col_qty_num = 'КоличествоBalance'
col_sklad_num = 'ЯчейкаХранения.Склад.Description'

col_ka_art = 'Unnamed: 0'
col_ka_name = 'Unnamed: 6'
col_ka_qty = 'Unnamed: 11'

dic_log_return = {'Расход': 0, 'Приход': 0, 'Доступы': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}


def start(_file_pg_stock, _contract):
    _ = str(_file_pg_stock).lower().find("брак")
    if str(_file_pg_stock).lower().find("брак") >= 0:
        brak = True
    else:
        brak = False
    try:
        _file_wms_stock = __get_file_wms_stock(contract=_contract)
        _df_wms = __get_wms_stock_wedlock(_file_wms=_file_wms_stock, _brak=brak)
        _df_ka = __get_ka_stock_wedlock(_file_ka_stock=_file_pg_stock)
        _df_compare = __compare_df(_df1=_df_wms, _df2=_df_ka)
        _file_name = __save_reports_stock_to_excel(_contract=_contract, _df_stocks_save=_df_compare,
                                                   _type_reports='Сверка')
        return _file_name
    except Exception as e:
        return {'error': str(e)}, True


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
    df = _df_new.dropna(subset=[_df_new.columns[1]])
    df.columns = df.iloc[3]
    df.rename(columns=lambda x: x.strip())
    df.drop(df.index[:4], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def __get_file_wms_stock(contract):
    __file_wms_stock = WmsStocks(_contract=contract).get_goods_by_guid_group(_contract=contract)
    return __file_wms_stock


def __get_wms_stock_wedlock(_file_wms, _brak):
    _df = pd.read_excel(_file_wms)
    _df_brak_ind = _df[_df['ЯчейкаХранения.Склад.Description'].str.contains(r"\брак\b", case=False)].index
    _df_brak = _df[_df['ЯчейкаХранения.Склад.Description'].str.contains(r"\брак\b", case=False)]

    _df_not_brak = _df.drop(index=_df_brak_ind, axis=1)
    _df_test = _df_not_brak[_df_not_brak['Номенклатура.Артикул'] == 'zld700001437'].copy()
    if _brak:
        _df = _df_brak
    else:
        _df = _df_not_brak

    _wms = pd.DataFrame()
    _wms['Артикул'] = _df[col_art_num].str.strip()
    _wms['Артикул'] = _wms['Артикул'].str.replace("zld", "")
    _wms['Наименование'] = _df[col_name_num]
    _wms['Кол-во склад'] = _df[col_qty_num]
    # df1 = _wms.drop_duplicates().groupby('Артикул', sort=False, as_index=False).sum()
    df1 = _wms.groupby(["Артикул"]).agg({
        "Кол-во склад": "sum",
        'Наименование': 'last'
    }).reset_index()
    return df1


def __get_ka_stock_wedlock(_file_ka_stock):
    _df = pd.read_excel(_file_ka_stock)
    _df = _df[_df['Unnamed: 6'].notna()].reset_index(drop=True)
    _df.drop(index=[0], axis=0, inplace=True)
    _ka = pd.DataFrame()
    _ka['Артикул'] = _df[col_ka_art].str.strip()
    _ka['_Наименование'] = _df[col_ka_name]
    _ka['Кол-во Зеландия'] = _df[col_ka_qty]
    _df1 = _ka.drop_duplicates().groupby('Артикул', sort=False, as_index=False).sum()
    return _df1


def __compare_df(_df1, _df2):
    _df_ = pd.merge(_df1, _df2, on='Артикул', how='outer').sort_values(by='Артикул')
    with pd.option_context("future.no_silent_downcasting", True):
        _df_merge = _df_.fillna(0).infer_objects(copy=False)
    _df_merge.fillna(0, inplace=True)
    _df_merge['Разница'] = _df_merge['Кол-во склад'] - _df_merge['Кол-во Зеландия']
    _df_merge.drop('_Наименование', axis=1, inplace=True)
    return _df_merge


dic_columns = {0: 'Артикул', 1: 'Номенклатура', 2: 'штрих-код шт', 3: 'штрих-код блок', 4: 'штрих-код короб',
               5: 'Вес нетто, шт', 6: 'Вес брутто, шт', 7: 'Количество шт. в коробе', 8: 'Количество шт. в блоке',
               9: 'Количество шт. в паллете', 10: 'Количество коробов на паллете', 11: 'Количество  коробов в слое',
               12: 'Длина шт. в мм', 13: 'Ширина шт. в мм', 14: 'Высота шт. в мм', 15: 'Обьем шт. в м3',
               16: 'Срок годности в днях', 17: 'Цена за шт. для расчетов убытков'}


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
    df_product['EanBarcodeBox'] = _df[dic_columns[2]]
    df_product['EanBarcodePack'] = _df[dic_columns[2]]
    df_product['Gs1Barcode'] = _df[dic_columns[2]]
    df_product['Gs1BarcodeBox'] = _df[dic_columns[2]]
    df_product['Gs1BarcodePack'] = _df[dic_columns[2]]
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, 'InventTable', contract=contract)
    dic_log_return['Справочник товаров'] += len(dic_product)
