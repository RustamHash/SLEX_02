import pandas as pd
from pg_sql.models import PgGoods
dic_log_return = {'Расход': 0, 'Приход': 0, 'Доступы': 0, 'Справочник товаров': 0, 'Справочник клиентов': 0}


def start(file_name, contract):
    return dic_log_return, True


def correction_date_pk_rnd(file_name, contract):
    _df_error = ''
    _df = pd.read_excel(file_name, dtype=object)
    _df['Разница'].astype(str).fillna('', inplace=True)
    _art_list = _df['Номенклатура.Артикул , Номенклатура'].unique().tolist()
    for _art in _art_list:
        _n_art = _df['Номенклатура.Артикул , Номенклатура'].value_counts()[_art]
    _df = _df.loc[_df.duplicated(subset=['Номенклатура.Артикул , Номенклатура'], keep=False), :]
    _df.reset_index(inplace=True)
    _df = _df.groupby(['Номенклатура.Артикул , Номенклатура', 'Дата производства'])['Разница'].sum().reset_index()
    if _df['Разница'].sum() != 0:
        _df_error = _df.groupby(['Номенклатура.Артикул , Номенклатура'])['Разница'].sum().reset_index()
    _df_order = _df[_df['Разница'] < 0].copy()
    _df_porder = _df[_df['Разница'] > 0].copy()
    _df_porder['Номенклатура.Артикул , Номенклатура'] = _df_porder['Номенклатура.Артикул , Номенклатура'].apply(
        lambda row: (row.split(',')[0]).strip())
    _df_order['Номенклатура.Артикул , Номенклатура'] = _df_order['Номенклатура.Артикул , Номенклатура'].apply(
        lambda row: (row.split(',')[0]).strip())
    _df_order.to_excel('расход.xlsx', index=False)
    _df_porder.to_excel('приход.xlsx', index=False)
    if isinstance(_df_error, pd.DataFrame):
        _df_error.to_excel('расхождения.xlsx', index=False)
    return _df_order, _df_porder, _df_error


def build_peresort(_file_name, _contract):
    _df = pd.read_excel(_file_name)
    _df.rename(columns={'Артикул': 'Код'}, inplace=True)
    _f = '_goods.xlsx'
    _df.to_excel(_f, index=False)
    _res = PgGoods().get_goods_list_by_marking_goods(_file_marking_goods=_f, _contract=_contract)
    # _res.to_excel(_f, index=False)
    return _res
