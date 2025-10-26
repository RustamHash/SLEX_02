import datetime
import locale
import os
import time


def save_reports_stock_to_excel(_contract, _df_stocks_save, _type_reports):
    _path_files = __exists_create_folder(_contract=_contract)
    _f_name = f"{_path_files}\\{__create_date_file_name()}_{_type_reports}_{_contract.name}.xlsx"
    _df_stocks_save.to_excel(f"{_f_name}", index=False)
    return _f_name


def __exists_create_folder(_contract):
    _dt_mouth, _dt_year = __create_date_folder_name()
    path_files = os.path.join(_contract.path_saved_reports, _dt_year, _dt_mouth)
    if not os.path.exists(path_files):
        os.makedirs(path_files)
    return path_files


def __create_date_file_name():
    _dt = datetime.datetime.now()
    _dt = _dt.strftime("%d%m%y%H%M%S")
    _dt = str(_dt)
    time.sleep(0.0006)
    return _dt


def __create_date_folder_name():
    locale.setlocale(locale.LC_TIME, "ru")
    _dt = datetime.datetime.now()
    _dt_mouth = _dt.strftime("%B")
    _dt_year = _dt.strftime("%Y")
    _dt_mouth = str(_dt_mouth)
    _dt_year = str(_dt_year)
    return _dt_mouth, _dt_year
