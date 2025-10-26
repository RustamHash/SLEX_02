import pandas as pd

from base_app.utils import data_to_dict, save_to_xml

dic_log_return = {
    "Расход": 0,
    "Приход": 0,
    "Справочник товаров": 0,
    "Справочник клиентов": 0,
}
dic_const = {
    "id_sklad": "16720849",
    "id_client": "16717331",
    "id_postav": "16717311",
    "delivery_type": 2,
}

ADD_PALLET = False


NUM_TYPE_ORDER = 0
NUM_DATE_ORDER = 1
NUM_DATE_PORDER = 1
NUM_ORDER = 2
NUM_ART_PRODUCT = 3
NUM_NAME_PRODUCT = 3
NUM_QTY_PRODUCT = 4
NUM_COMMENT = 5


def start(file_name, contract):
    try:
        for i in dic_log_return:
            dic_log_return[i] = 0
        _df_order, _df_porder = __load_parse_file(file_name)
        print(f"order: \n {_df_order.to_markdown()}")
        print(f"porder: \n {_df_porder.to_markdown()}")
        if len(_df_order) > 0:
            __create_order(_df_order, contract)
        if len(_df_porder) > 0:
            __create_porder(_df_porder, contract)
        return dic_log_return, True
    except Exception as e:
        return {"error": str(e)}, False


def __load_parse_file(_wb_file):
    _df = pd.read_excel(_wb_file, dtype=object)
    _df_order = _df[_df[_df.columns[NUM_TYPE_ORDER]] == "IN"].copy()
    _df_porder = _df[_df[_df.columns[NUM_TYPE_ORDER]] == "OUT"].copy()
    return _df_order, _df_porder


def __create_order(_df, contract):
    df_order = pd.DataFrame()
    df_order["Itemid"] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_order["Qty"] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_order["SalesId"] = _df[_df.columns[NUM_ORDER]]
    df_order["InventLocationId"] = dic_const["id_sklad"]
    df_order["ConsigneeAccount"] = dic_const["id_client"]
    df_order["DeliveryDate"] = _df[_df.columns[NUM_DATE_ORDER]]
    df_order["ManDate"] = _df[_df.columns[NUM_DATE_ORDER]]
    df_order["SalesUnit"] = "шт"
    df_order["Delivery"] = dic_const["delivery_type"]
    df_order["Redelivery"] = 1
    df_order["OrderType"] = 1
    df_order["Comment"] = _df[_df.columns[NUM_COMMENT]]
    dic_order = data_to_dict(df_order)
    save_to_xml(dic_order, "CustPicking", contract=contract)
    dic_log_return["Расход"] += len(dic_order)


def __create_porder(_df, contract):
    df_porder = pd.DataFrame()
    df_porder["Itemid"] = _df[_df.columns[NUM_ART_PRODUCT]]
    df_porder["Qty"] = _df[_df.columns[NUM_QTY_PRODUCT]]
    df_porder["PurchId"] = _df[_df.columns[NUM_ORDER]]
    df_porder["VendAccount"] = dic_const["id_postav"]
    df_porder["DeliveryDate"] = _df[_df.columns[NUM_DATE_PORDER]]
    df_porder["InventLocationId"] = dic_const["id_sklad"]
    df_porder["ProductionDate"] = "01.01.2025"
    df_porder["PurchUnit"] = "шт"
    df_porder["PurchTTN"] = _df[_df.columns[NUM_ORDER]]
    df_porder["Price"] = 0
    df_porder["Comment"] = _df[_df.columns[NUM_COMMENT]]
    dic_order = data_to_dict(df_porder)
    save_to_xml(dic_order, "VendReceipt", contract=contract)
    dic_log_return["Приход"] += len(dic_order)


def __create_product(_df, contract):
    df_product = pd.DataFrame()
    df_product["ItemId"] = _df[_df.columns[0]]
    df_product["ItemName"] = _df[_df.columns[1]].astype(str)
    df_product["NetWeight"] = _df[_df.columns[5]]
    df_product["NetWeightBox"] = 500
    df_product["NetWeightPack"] = 500
    df_product["BruttoWeight"] = _df[_df.columns[5]]
    df_product["BruttoWeightBox"] = 500
    df_product["BruttoWeightPack"] = 500
    df_product["Quantity"] = _df[_df.columns[7]]
    df_product["standardShowBoxQuantity"] = 1
    df_product["UnitId"] = "шт"
    df_product["Depth"] = _df[_df.columns[13]]
    df_product["Height"] = _df[_df.columns[15]]
    df_product["Width"] = _df[_df.columns[14]]
    df_product["BoxDepth"] = 0
    df_product["BoxHeight"] = 0
    df_product["BoxWidth"] = 0
    df_product["BlockDepth"] = 0
    df_product["BlockHeight"] = 0
    df_product["BlockWidth"] = 0
    df_product["StandardPalletQuantity"] = _df[_df.columns[11]]
    df_product["QtyPerLayer"] = 1
    df_product["Price"] = _df[_df.columns[18]]
    df_product["ShelfLife"] = _df[_df.columns[17]]
    df_product["EanBarcode"] = _df[_df.columns[2]]
    df_product["EanBarcodeBox"] = _df[_df.columns[4]]
    df_product["EanBarcodePack"] = _df[_df.columns[4]]
    df_product["Gs1Barcode"] = 0
    df_product["Gs1BarcodeBox"] = 0
    df_product["Gs1BarcodePack"] = 0
    dic_product = data_to_dict(df_product)
    save_to_xml(dic_product, "InventTable", contract=contract)
    dic_log_return["Справочник товаров"] += len(dic_product)
