import requests
import pandas as pd
from tkinter import filedialog
import datetime
import xml.etree.ElementTree as et
from xml.dom import minidom

list_columns = ['Номер', 'От кого', 'Адрес доставки']

file_name_save = 'agro11.xml'

TYPE_DELIVERY = '007'
DRIVER = '_'
LoadingNum = '10'
LoadingTime = '_'
TruckID = '_'

dic_log_return = {'Маршруты': 0}
error_dict = {}


def start(file_name, contract):
    error_dict.clear()
    try:
        for key, value in dic_log_return.items():
            dic_log_return[key] = 0
        df = __load_file(file_name)
        __flag = __response_columns_file(df)
        if __flag:
            if df.shape[0] >= 1:
                x = __parse_dataframe(df)
                if x:
                    __create_structura_xml(x)
                    res = __post()
                    list_deliver = __parse_response_xml(res)
                    dic_log_return['Маршруты'] += len(list_deliver)
                else:
                    error_dict['Ошибка xml'] = f'Ошибка создания xml файла!'
            else:
                error_dict['Ошибка файла'] = f'Ошибка чтения файла {file_name}'
        if len(error_dict) > 0:
            return error_dict, False
        else:
            return dic_log_return, True
    except Exception as e:
        error_dict['Ошибка: '] = str(e)
        return error_dict, False


def __parse_response_xml(response):
    __list_deliver = []
    response_body_as_xml = et.fromstring(response.content)
    for number in response_body_as_xml.iter('Number'):
        __list_deliver.append(number.text)
    return __list_deliver


def __response_columns_file(__df):
    __columns = __df.columns
    __er = 0
    for column in list_columns:
        if column in __columns:
            __er += 1
        else:
            error_dict['Ошибка данных'] = (f'Отсутствует колонка с наименованием {column}!\n'
                                           f'Обязательные поля для создания маршрутов {list_columns}')
            return False
    return True


def __get_file():
    __file_name = filedialog.askopenfilenames()
    return __file_name


def __load_file(__filename):
    __df = pd.read_excel(__filename)
    return __df


def __parse_dataframe(__df):
    __dict_delivery = {}
    try:
        __df['Адрес доставки'] = ('AGRO' + '_' + __df['От кого'] + "_" + __df['Адрес доставки'])
        __keys = __df['Адрес доставки'].to_list()
        keys = set(__keys)
        for key in keys:
            _df = __df[__df['Адрес доставки'] == key]
            list_num_order = _df['Номер'].to_list()
            __dict_delivery[key] = list_num_order
        return __dict_delivery
    except:
        return False


def __create_date():
    _dt = datetime.datetime.now().date() + datetime.timedelta(days=1)
    _dt = str(_dt)
    return _dt


def __save_xml(xml_code):
    xml_string = et.tostring(xml_code).decode()
    xml_prettyxml = minidom.parseString(xml_string).toprettyxml()
    with open(file_name_save, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_prettyxml)


def __create_number():
    # _dt = datetime.datetime.now().date() + datetime.timedelta(days=1)
    _dt = datetime.datetime.now().date()
    _str_dt = _dt.strftime('%d%m%Y')
    return _str_dt


def __create_sklad(data: str):
    if len(data) > 0:
        try:
            if 'Заморозка' in data:
                sklad = 'Заморозка'
                return sklad
            else:
                sklad = 'Сухой'
                return sklad
        except:
            error_dict['Ошибка склад'] = 'Ошибка чтения склада!'
            return False
    else:
        error_dict['Ошибка склад'] = 'Передано пустое значение склада!'


def __create_structura_xml(data: dict):
    _dt = __create_date()
    new = et.Element('xml')
    new.attrib = {'version': "1.0", 'encoding': "utf-8"}
    message = et.SubElement(new, 'Message')
    base_id = et.SubElement(message, 'BaseID')
    base_id.text = 'AGRO'

    documents = et.SubElement(message, 'Documents')
    for i, key in enumerate(data):
        document = et.SubElement(documents, 'Document')
        type_delivery = et.SubElement(document, 'Type')
        type_delivery.text = TYPE_DELIVERY
        number = et.SubElement(document, 'Number')
        number.text = __create_number() + "_" + str(i + 1)
        date = et.SubElement(document, 'Date')
        date.text = __create_date()
        driver = et.SubElement(document, 'Driver')
        # driver.text = str(key)
        driver.text = key.split('_')[-1]
        login_num = et.SubElement(document, 'LoadingNum')
        login_num.text = LoadingNum
        login_time = et.SubElement(document, 'LoadingTime')
        login_time.text = LoadingTime
        truc_id = et.SubElement(document, 'TruckID')
        # truc_id.text = TruckID
        # truc_id.text = str(key)
        truc_id.text = __create_sklad(str(key))
        comment = et.SubElement(document, 'Comment')
        comment.text = str(key)
        order = et.SubElement(document, 'Orders')
        for v in data[key]:
            row = et.SubElement(order, 'row')
            order_base_id = et.SubElement(row, 'BaseID')
            order_base_id.text = '376'
            type_order = et.SubElement(row, 'Type')
            type_order.text = '001'
            rout = et.SubElement(row, 'Rout')
            rout.text = str(key)
            number = et.SubElement(row, 'Number')
            number.text = str(v)
            weight = et.SubElement(row, 'Weight')
            weight.text = '1'
    __save_xml(new)


def __post():
    headers = {'Authorization': 'Basic RXhjaGFuZ2VXTVM6YWY1Njc0ODY=',
               'Content-Type': 'application/xml',
               'Accept-Encoding': 'gzip, deflate, br'}
    # login = 'ExchangeWMS'
    # password = 'af567486'
    session = requests.Session()
    url = 'http://172.172.185.67/krd_itc_wms/ru_RU/hs/PutData'
    with open(file_name_save, 'rb') as file:
        # __res = session.post(url, headers=headers, data=file)
        __res = requests.post(url, headers=headers, data=file)
    return __res
