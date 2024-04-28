import datetime
import locale
import os

import psycopg2 as ps
import pandas as pd


def get_good_by_marking_goods(_marking_goods, _contract):
    _sql = f"SELECT marking_goods AS Артикул, item_name AS Наименование FROM goods_all WHERE marking_goods={_marking_goods}"
    _dsn = _contract.filial.dsn
    res_df_by_good = __connect_to_db(_dsn=_dsn, _sql=_sql)
    return res_df_by_good


def get_goods_list_by_marking_goods(_file_marking_goods, _contract):
    _df_load = pd.read_excel(_file_marking_goods, dtype=object)
    _list__marking_goods = _df_load['Код'].values.tolist()
    _to_list_marking_goods = tuple(_list__marking_goods)
    _sql = ("SELECT marking_goods AS Артикул, item_name AS Наименование FROM goods_all "
            "WHERE marking_goods IN {}").format(_list__marking_goods)
    _dsn = _contract.filial.connect_pg_str
    res_df_goods = __connect_to_db(_dsn=_dsn, _sql=_sql)
    return res_df_goods


def query_goods_stock_by_group_id(id_group_goods, _contract):
    _prog_id = _contract.filial.prog_id
    _dsn = _contract.filial.dsn
    _sql = (
        "SELECT skl.item_name AS Склад, skl.id, gds.marking_goods AS Артикул, gds.item_name AS Наименование, rst.goods_id AS КодТовара,"
        "rst.pull_date AS СрокГодности, rst.man_date AS ДатаИзготовления,gds.shelf_life AS СрокГодностиДни,rst.price AS ЦенаИзПрихода,"
        "SUM(rst.items_count) AS Количество "
        "FROM s_rt rst "
        "JOIN store.agent skl ON rst.store_id=skl.id "
        "JOIN goods_all gds ON rst.goods_id=gds.id "
        f"WHERE rst.program_id={_prog_id} AND gds.group_id={id_group_goods} "
        "GROUP BY rst.goods_id, skl.item_name, gds.item_name, gds.marking_goods, skl.id, "
        "rst.pull_date, rst.man_date, gds.shelf_life, rst.price "
        "ORDER BY skl.item_name, rst.goods_id"
    )

    res_df_stocks = __connect_to_db(_sql=_sql, _dsn=_dsn)
    return res_df_stocks


def query_goods_stock_by_group_id_ok(id_group_goods, _contract):
    _list_file_name = []
    _prog_id = _contract.filial.prog_id
    _dsn = _contract.filial.dsn
    _sql = (
        "SELECT skl.item_name AS Склад, skl.id, gds.marking_goods AS Артикул, gds.item_name AS Наименование, rst.goods_id AS КодТовара,"
        "rst.pull_date AS СрокГодности, rst.man_date AS ДатаИзготовления,gds.shelf_life AS СрокГодностиДни,rst.price AS ЦенаИзПрихода,"
        "SUM(rst.items_count) AS Количество "
        "FROM s_rt rst "
        "JOIN store.agent skl ON rst.store_id=skl.id "
        "JOIN goods_all gds ON rst.goods_id=gds.id "
        f"WHERE rst.program_id={_prog_id} AND gds.group_id IN (SELECT id FROM gds WHERE gds.group_id={id_group_goods}) "
        "GROUP BY rst.goods_id, skl.item_name, gds.item_name, gds.marking_goods, skl.id, "
        "rst.pull_date, rst.man_date, gds.shelf_life, rst.price "
        "ORDER BY skl.item_name, rst.goods_id"
    )
    res_df_stocks = __connect_to_db(_sql=_sql, _dsn=_dsn)
    _sql_vod = "SELECT id FROM store.agent WHERE group_id IN (17003663, 17012968)"
    res_df_store_vod = __connect_to_db(_sql=_sql, _dsn=_dsn)
    res_df_store_vod['id'] = res_df_store_vod['id'].astype(int)
    _l_store_vod = res_df_store_vod['id'].values.tolist()

    def check_tax_class(row):
        if row['id'] in _l_store_vod:
            return 'Водители'
        else:
            return row['Склад']

    res_df_stocks['Склад'] = res_df_stocks.apply(check_tax_class, axis=1)
    return res_df_stocks


def __save_reports_stock(_df_stock_all, _contract):
    _path_files = __exists_create_folder(_contract.path_saved_reports)
    _list_df_stock_all = []
    _stores = _df_stock_all['Склад'].unique().tolist()
    for _stor in _stores:
        _df_ = _df_stock_all[_df_stock_all['Склад'] == _stor].copy()
        _df_.reset_index(inplace=True, drop=True)
        _df_.drop(['id', 'КодТовара'], axis=1, inplace=True)
        _f_name = f'{_path_files}\\{__create_date()}_{str(_stor)}.xlsx'
        _df_.to_excel(f'{_f_name}', index=False)
        _list_df_stock_all.append(_f_name)
    return _list_df_stock_all


def __create_date():
    _dt = datetime.datetime.now() - datetime.timedelta(days=1)
    _dt = _dt.strftime("%d%m%y")
    _dt = str(_dt)
    return _dt


def __create_date_folder_name():
    locale.setlocale(locale.LC_TIME, 'ru')
    _dt = datetime.datetime.now() - datetime.timedelta(days=1)
    _dt_mouth = _dt.strftime("%B")
    _dt_year = _dt.strftime("%Y")
    _dt_mouth = str(_dt_mouth)
    _dt_year = str(_dt_year)
    return _dt_mouth, _dt_year


def __exists_create_folder(folder_name):
    _dt_mouth, _dt_year = __create_date_folder_name()
    path_files = os.path.join(folder_name, _dt_year, _dt_mouth)
    if not os.path.exists(path_files):
        os.makedirs(path_files)
    return path_files


def __connect_to_db(_dsn, _sql):
    with ps.connect(_dsn) as conn:
        _df_query = pd.read_sql_query(sql=_sql, con=conn)
        return _df_query
