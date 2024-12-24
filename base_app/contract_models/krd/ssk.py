import pandas as pd
from base_app.utils import data_to_dict, save_to_xml, dic_log_return
from base_app.contract_models import standart


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
            standart.__create_order(_df_order, contract)
        if len(_df_porder) > 0:
            standart.__create_porder(_df_porder, contract)
            standart.__create_product(_df_porder, contract)
        return dic_log_return, True
    except Exception as e:
        return {'error': str(e)}, False


def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype=object)
    _df[_df.columns[NUM_ART_PRODUCT]] = _df[_df.columns[NUM_ART_PRODUCT]].str.replace(' ', '')
    _df[_df.columns[NUM_ART_PRODUCT]] = _df[_df.columns[NUM_ART_PRODUCT]].str.replace('\'', '')
    _df[_df.columns[NUM_NAME_PRODUCT]] = _df[_df.columns[NUM_NAME_PRODUCT]].str.replace('\'', '')
    _df_order = _df[_df['ВидНакладной'] == 'Расход'].copy()
    _df_porder = _df[_df['ВидНакладной'] == 'Приход'].copy()
    return _df_order, _df_porder
