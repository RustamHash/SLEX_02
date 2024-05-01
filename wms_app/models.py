import datetime
import json
import locale
import os

import pandas as pd
import requests


class SaveFileWms:
    def __init__(self):
        super(SaveFileWms, self).__init__()
        self.json_stocks_wms = None
        self.contract_wms = None

    def save_reports_stock(self):
        _path_files = self.__exists_create_folder()
        _f_name = f'{_path_files}\\{self.__create_date_file_name()}_{self.contract_wms}_wms.xlsx'
        _df = pd.json_normalize(self.json_stocks_wms)
        _df.to_excel(f'{_f_name}', index=False)
        return _f_name

    @staticmethod
    def __validate_file_name(file_name):
        file_name = str(file_name)
        file_name = file_name.replace('"', "").replace("'", "")
        file_name = file_name.lower()
        return file_name

    @staticmethod
    def __create_date_file_name():
        _dt = datetime.datetime.now()
        _dt = _dt.strftime("%d%m%y")
        _dt = str(_dt)
        return _dt

    @staticmethod
    def __create_date_folder_name():
        locale.setlocale(locale.LC_TIME, 'ru')
        _dt = datetime.datetime.now()
        _dt_mouth = _dt.strftime("%B")
        _dt_year = _dt.strftime("%Y")
        _dt_mouth = str(_dt_mouth)
        _dt_year = str(_dt_year)
        return _dt_mouth, _dt_year

    def __exists_create_folder(self):
        _dt_mouth, _dt_year = self.__create_date_folder_name()
        path_files = os.path.join(f'{self.contract_wms.path_saved_reports}_wms', _dt_year, _dt_mouth)
        if not os.path.exists(path_files):
            os.makedirs(path_files)
        return path_files


class WmsKrd:
    def __init__(self, ):
        super(WmsKrd, self).__init__()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        self.server = '172.172.185.67'
        self.infobase = 'krd_itc_wms'
        self.username = 'ODUser'
        self.password = 249981
        self.params = None
        self.contract_wms = None
        self.json_data = None
        self.full_url = f"http://{self.server}/{self.infobase}/odata/standard.odata/"
        self._auth = requests.auth.HTTPBasicAuth(self.username, self.password)

    def connect(self, _top=None):
        if _top is not None:
            if self.params is None:
                self.params = f"$top={_top}"
            else:
                self.params = f"{self.params}&$top={_top}"
        response = requests.get(url=self.full_url, headers=self.headers, auth=self._auth, params=self.params)
        return response


class WmsStocks(WmsKrd, SaveFileWms):
    def __init__(self):
        super(WmsStocks, self).__init__()
        self.cat_name = 'ОстаткиВПоллетах'
        self.params = (f"$select="
                       f"Номенклатура/Code,"
                       f"Номенклатура/Description,"
                       f"Номенклатура/Артикул,"
                       f"Номенклатура/Parent/Description,"
                       f"КоличествоBalance"
                       f"&$orderby=Номенклатура/Артикул"
                       )
        self.full_url = (f'{self.full_url}/AccumulationRegister_{self.cat_name}/Balance?'
                         f'$format=json&$expand=Номенклатура/Parent'
                         )

    def get_good_by_art(self, good_art, _contract):
        self.contract_wms = _contract
        self.params = f"{self.params}&$filter=Номенклатура/Артикул eq'{good_art}'"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name

    def get_goods_by_guid_group(self, _contract, top=None):
        self.contract_wms = _contract
        self.params = f"{self.params}&$filter=Номенклатура/Parent/Code eq '{str(self.contract_wms.id_groups_goods)}'"
        if top is not None:
            self.params = f"{self.params}&$top={top}"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name


class WmsGoods(WmsKrd, SaveFileWms):
    def __init__(self):
        super(WmsGoods, self).__init__()
        self.cat_name = 'Номенклатура'
        self.params = f"$select=Ref_Key,Parent_Key,Code,Description,Артикул"
        self.full_url = f'{self.full_url}/Catalog_{self.cat_name}'

    def get_good_by_art(self, good_art, _contract):
        self.contract_wms = _contract
        self.params = f"{self.params}&$filter=Артикул eq'{good_art}'"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name

    def get_goods_by_guid_group(self, _contract, top=None):
        self.contract_wms = _contract
        self.params = f"{self.params}&$filter=Parent_Key eq '{str(self.contract_wms.id_groups_goods)}'"
        if top is not None:
            self.params = f"{self.params}&$top={top}"
        response = self.connect()
        if response.status_code != 200:
            return response.text
        self.json_stocks_wms = json.loads(response.text).get('value', None)
        _file_name = self.save_reports_stock()
        return _file_name
