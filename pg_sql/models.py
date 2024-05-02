import datetime
import locale
import os

import psycopg2 as ps
import pandas as pd


class SaveFile:
    def __init__(self):
        super(SaveFile, self).__init__()
        self.df_stocks_save = None
        self.contract_save = None

    def save_reports_stock_ok(self):
        _path_files = self.__exists_create_folder()
        _list_df_stock_all = []
        _stores = self.df_stocks_save['Склад'].unique().tolist()
        for _stor in _stores:
            _df_ = self.df_stocks_save[self.df_stocks_save['Склад'] == _stor].copy()
            _df_.reset_index(inplace=True, drop=True)
            if 'id' in _df_.columns and 'КодТовара' in _df_.columns:
                _df_.drop(['id', 'КодТовара'], axis=1, inplace=True)
            _file_name = self.__validate_file_name(_stor)
            _f_name = f'{_path_files}\\{self.__create_date_file_name()}_{str(_file_name)}.xlsx'
            _df_.to_excel(f'{_f_name}', index=False)
            _list_df_stock_all.append(_f_name)
        return _list_df_stock_all

    def save_reports_stock(self):
        _path_files = self.__exists_create_folder()
        if 'id' in self.df_stocks_save.columns:
            self.df_stocks_save.drop(['id'], axis=1, inplace=True)
        _f_name = f'{_path_files}\\{self.__create_date_file_name()}_{self.contract_save}.xlsx'
        self.df_stocks_save.to_excel(f'{_f_name}', index=False)
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
        path_files = os.path.join(self.contract_save.path_saved_reports, _dt_year, _dt_mouth)
        if not os.path.exists(path_files):
            os.makedirs(path_files)
        return path_files


class PgConnection:
    def __init__(self):
        self._dsn = None
        self._sql = None
        self._select = "SELECT "
        self._from = " FROM "
        self._where = " WHERE "
        self._order = " ORDER "

    def connect(self):
        with ps.connect(self._dsn) as conn:
            _df_query = pd.read_sql_query(sql=self._sql, con=conn)
            return _df_query


class PgGoods(PgConnection, SaveFile):
    def __init__(self):
        super(PgGoods, self).__init__()

    def get_good_by_marking_goods(self, _marking_goods, _contract):
        self.contract_save = _contract
        self._sql = f"SELECT marking_goods AS Артикул, item_name AS Наименование FROM goods_all WHERE marking_goods='{str(_marking_goods)}'"
        self._dsn = self.contract_save.filial.url_pg
        self.df_stocks_save = self.connect()
        _file_name_stock = self.save_reports_stock()
        return _file_name_stock

    def get_goods_list_by_marking_goods(self, _file_marking_goods, _contract, _top=None):
        self.contract_save = _contract
        _df_load = pd.read_excel(_file_marking_goods, dtype=object)
        _list__marking_goods = _df_load['Код'].values.tolist()
        if len(_list__marking_goods) == 1:
            _list__marking_goods.append(_list__marking_goods[0])
        _to_list_marking_goods = tuple(_list__marking_goods)
        self._sql = ("SELECT marking_goods AS Артикул, item_name AS Наименование FROM goods_all "
                     "WHERE marking_goods IN {}").format(_to_list_marking_goods)
        self._dsn = self.contract_save.filial.url_pg
        if _top is not None:
            self._sql = f'{self._sql} LIMIT {_top}'
        self.df_stocks_save = self.connect()
        _file_name_stock = self.save_reports_stock()
        return _file_name_stock


class PgStocks(PgConnection, SaveFile):
    def __init__(self):
        super(PgStocks, self).__init__()

    def query_goods_stock_by_group_id(self, _contract, top=None):
        self.contract_save = _contract
        _prog_id = self.contract_save.filial.prog_id
        self._dsn = self.contract_save.filial.url_pg
        _id_group_goods = self.contract_save.id_groups_goods
        self._sql = (
            "SELECT skl.item_name AS Склад, skl.id, gds.marking_goods AS Артикул, gds.item_name AS Наименование, rst.goods_id AS КодТовара,"
            "rst.pull_date AS СрокГодности, rst.man_date AS ДатаИзготовления,gds.shelf_life AS СрокГодностиДни,rst.price AS ЦенаИзПрихода,"
            "SUM(rst.items_count) AS Количество "
            "FROM s_rt rst "
            "JOIN store.agent skl ON rst.store_id=skl.id "
            "JOIN goods_all gds ON rst.goods_id=gds.id "
            f"WHERE rst.program_id={_prog_id} AND gds.group_id={_id_group_goods} "
            "GROUP BY rst.goods_id, skl.item_name, gds.item_name, gds.marking_goods, skl.id, "
            "rst.pull_date, rst.man_date, gds.shelf_life, rst.price "
            "ORDER BY skl.item_name, rst.goods_id"
        )
        if top is not None:
            self._sql = f'{self._sql} LIMIT {top}'
        self.df_stocks_save = self.connect()
        print(self.df_stocks_save)
        _file_name_stock = self.save_reports_stock()
        return _file_name_stock

    def query_goods_stock_by_group_id_ok(self, _contract, top=None):
        self.contract_save = _contract
        _list_file_name = []
        _prog_id = self.contract_save.filial.prog_id
        _id_group_goods = self.contract_save.id_groups_goods
        self._dsn = self.contract_save.filial.url_pg
        self._sql = (
            "SELECT skl.item_name AS Склад, skl.id, gds.marking_goods AS Артикул, gds.item_name AS Наименование, rst.goods_id AS КодТовара,"
            "rst.pull_date AS СрокГодности, rst.man_date AS ДатаИзготовления,gds.shelf_life AS СрокГодностиДни,rst.price AS ЦенаИзПрихода,"
            "SUM(rst.items_count) AS Количество "
            "FROM s_rt rst "
            "JOIN store.agent skl ON rst.store_id=skl.id "
            "JOIN goods_all gds ON rst.goods_id=gds.id "
            f"WHERE rst.program_id={_prog_id} AND gds.group_id IN (SELECT id FROM goods_all WHERE group_id= {_id_group_goods})"
            "GROUP BY rst.goods_id, skl.item_name, gds.item_name, gds.marking_goods, skl.id, "
            "rst.pull_date, rst.man_date, gds.shelf_life, rst.price "
            "ORDER BY skl.item_name, rst.goods_id"
        )
        if top is not None:
            self._sql = f'{self._sql} LIMIT {top}'
        self.df_stocks_save = self.connect()
        self._sql = "SELECT id FROM store.agent WHERE group_id IN (17003663, 17012968)"
        res_df_store_vod = self.connect()
        res_df_store_vod['id'] = res_df_store_vod['id'].astype(int)
        _l_store_vod = res_df_store_vod['id'].values.tolist()

        def check_store_chauffeur(row):
            if row['id'] in _l_store_vod:
                return 'Водители'
            else:
                return row['Склад']

        self.df_stocks_save['Склад'] = self.df_stocks_save.apply(check_store_chauffeur, axis=1)
        _file_name_list = self.save_reports_stock_ok()
        return _file_name_list
