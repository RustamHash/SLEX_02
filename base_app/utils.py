import datetime
import locale
import os
import xml.etree.ElementTree as ET
from pprint import pprint
from xml.dom import minidom

import pandas as pd

prefix_type_order = {1: 'CustPicking', 0: 'VendReceipt'}


def comparison_stock(__file_pg_stock, __file_wms_stock, _contract):
    __df_pg_stock = pd.read_excel(__file_pg_stock)
    __df_wms_stock = pd.read_excel(__file_wms_stock)
    dict_col = {'Номенклатура.Артикул': 'Артикул',
                'Номенклатура.Description': 'Наименование',
                'Номенклатура.Code': 'КодТовара',
                'КоличествоBalance': 'Количество_WMS'
                }
    __df_wms_stock.rename(columns=dict_col, inplace=True)
    __df_pg_stock_by = __df_pg_stock.groupby(['Артикул', 'КодТовара', 'Наименование'])['Количество'].sum().reset_index()
    __df_wms_stock_by = __df_wms_stock.groupby(['Артикул', 'КодТовара', 'Наименование'])[
        'Количество_WMS'].sum().reset_index()
    df = __df_pg_stock_by.merge(__df_wms_stock_by, how='outer')
    df.fillna(0, inplace=True)
    df['Разница'] = df['Количество_WMS'] - df['Количество']
    _file_name = __save_reports_stock_to_excel(_contract=_contract, _df_stocks_save=df, _type_reports='Сверка')
    return _file_name


def data_to_dict(df):
    dic_order = {}
    name_col = 'SalesId'
    if 'SalesId' in df.columns:
        name_col = 'SalesId'
    elif 'PurchId' in df.columns:
        name_col = 'PurchId'
    elif 'Quantity' in df.columns:
        name_col = 'ItemId'
    elif 'CustVendID' in df.columns:
        name_col = 'CustVendID'
    for i in df[name_col]:
        dic_order[i] = None
    for key in dic_order.keys():
        _df = df[df[name_col] == key].copy()
        dic_order[key] = _df.to_dict('index')
    return dic_order


# def start_client(data: dict, key_contract):
#     key_contract = __update_name_contract(key_contract)
#     type_order = 'CustVendTable'
#     const_name = f'{str(type_order)}ExportDC'
#     _dt = __create_datetime()
#     new = ET.Element('AxaptaXMLExport')
#     x = str("urn:www.navision.com/Formats/Table")
#     y = str("1.0")
#     new.attrib = {'xmlns:Table': x, 'version': y}
#     title = ET.SubElement(new, 'transaction')
#     title.attrib = {'version': y}
#     for key, value in data.items():
#         title1 = ET.SubElement(title, 'Table:Record')
#         title1.attrib = {'name': const_name, 'row': str(key + 1)}
#         for k, v in value.items():
#             row = ET.SubElement(title1, 'Table:Field')
#             row.attrib = {'name': k}
#             row.text = str(v)
#     save_file_name = __create_name_file_save(str(_dt), str(type_order))
#     __save_xml(save_file_name, new)


def save_to_xml(data: dict, type_order, contract):
    for k1, v1 in data.items():
        const_name = f'{str(type_order)}ExportDC'
        new = ET.Element('AxaptaXMLExport')
        x = str("urn:www.navision.com/Formats/Table")
        y = str("1.0")
        new.attrib = {'xmlns:Table': x, 'version': y}
        title = ET.SubElement(new, 'transaction')
        title.attrib = {'version': y}
        for key, value in data[k1].items():
            title1 = ET.SubElement(title, 'Table:Record')
            title1.attrib = {'name': const_name, 'row': str(key + 1)}
            for k, v in value.items():
                row = ET.SubElement(title1, 'Table:Field')
                row.attrib = {'name': k}
                row.text = str(v)
        save_file_name = __create_name_file_save_xml(str(k1), str(type_order), contract)
        __save_xml(save_file_name, new)


def __save_reports_stock_to_excel(_contract, _df_stocks_save, _type_reports):
    _path_files = __exists_create_folder(_contract=_contract)
    _f_name = f'{_path_files}\\{__create_date_file_name()}_{_type_reports}_{_contract.name}.xlsx'
    _df_stocks_save.to_excel(f'{_f_name}', index=False)
    return _f_name


def __save_xml(filename, xml_code):
    xml_string = ET.tostring(xml_code).decode()
    xml_prettyxml = minidom.parseString(xml_string).toprettyxml()
    with open(filename, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_prettyxml)


def __create_name_file_save_xml(filename, const_name, contract):
    dt = __create_date_file_name()
    wb_path = contract.path_saved_order
    _path = f'{wb_path}\\{const_name}_{filename}_{filename}_{dt}.xml'
    return _path


def __create_date_folder_name():
    locale.setlocale(locale.LC_TIME, 'ru')
    _dt = datetime.datetime.now()
    _dt_mouth = _dt.strftime("%B")
    _dt_year = _dt.strftime("%Y")
    _dt_mouth = str(_dt_mouth)
    _dt_year = str(_dt_year)
    return _dt_mouth, _dt_year


def __create_date_file_name():
    _dt = datetime.datetime.now()
    _dt = _dt.strftime("%d%m%y")
    _dt = str(_dt)
    return _dt


def __validate_file_name(file_name):
    file_name = str(file_name)
    file_name = file_name.replace('"', "").replace("'", "")
    file_name = file_name.lower()
    return file_name


def __exists_create_folder(_contract):
    _dt_mouth, _dt_year = __create_date_folder_name()
    path_files = os.path.join(_contract.path_saved_reports, _dt_year, _dt_mouth)
    if not os.path.exists(path_files):
        os.makedirs(path_files)
    return path_files
