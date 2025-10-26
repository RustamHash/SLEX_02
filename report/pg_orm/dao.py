from datetime import datetime

import pandas as pd
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from report.pg_orm.database import session_krd, session_rnd, session_vlg
from report.pg_orm.models import Invoice, InvoiceBody, Agent, Goods

session_dict = {"krd": session_krd, "rnd": session_rnd, "vlg": session_vlg}


class BaseDao:
    model = None
    filial = None

    @classmethod
    def get_instance(cls, filter_params=None, limit: int = 1000):
        with session_dict[cls.filial]() as session:
            if filter_params is None:
                filter_params = {}
            query = select(cls.model).filter_by(**filter_params).limit(limit)
            res = session.execute(query)
            result = res.scalars().all()
            return result


class InvoiceDao(BaseDao):
    model = Invoice
    filial = None

    @classmethod
    def get_invoice(
        cls,
        filter_params=None,
        start_date=None,
        end_date=None,
        agent_id=None,
        program_id=None,
        delivery=None,
        limit: int = 1000,
    ):
        my_filters = set()

        if hasattr(cls.model, "agent_id"):
            if agent_id:
                my_filters.add(cls.model.agent_id == agent_id)
        if hasattr(cls.model, "program_id"):
            if program_id:
                my_filters.add(cls.model.program_id == program_id)
        if hasattr(cls.model, "delivery"):
            if delivery:
                my_filters.add(cls.model.delivery == delivery)
        if hasattr(cls.model, "date_doc"):
            if start_date:
                if end_date:
                    my_filters.add(cls.model.date_doc.between(start_date, end_date))
                else:
                    my_filters.add(
                        cls.model.date_doc.between(start_date, datetime.today())
                    )
            else:
                if end_date:
                    my_filters.add(
                        cls.model.date_doc.between(
                            datetime(datetime.today().year, 1, 1), end_date
                        )
                    )
                else:
                    my_filters.add(
                        cls.model.date_doc.between(
                            datetime(datetime.today().year, 1, 1), datetime.today()
                        )
                    )
        if filter_params is None:
            filter_params = {}
        with session_dict[cls.filial]() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_params)
                .filter(and_(*my_filters))
                .limit(limit)
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            return result

    @classmethod
    def get_detail_invoice(
        cls,
        filter_params=None,
        start_date=None,
        end_date=None,
        agent_id=None,
        program_id=None,
        delivery=None,
        limit: int = 1000,
    ):
        invoice_body_list = cls.get_invoice(
            filter_params=filter_params,
            start_date=start_date,
            end_date=end_date,
            agent_id=agent_id,
            program_id=program_id,
            delivery=delivery,
            limit=limit,
        )
        data_invoice_detail = []
        for invoice in invoice_body_list:
            if invoice.invoice_type_id == 203:
                if invoice.to_ids.dovoz:
                    agent_dovoz_name = invoice.to_ids.dovoz.item_name
                else:
                    agent_dovoz_name = "Error"
            else:
                agent_dovoz_name = "Приход"
            inv = {
                "acs_number": invoice.acs_number,
                "order_number": invoice.order_number,
                "date_doc": invoice.date_doc,
                "invoice_type_id": invoice.invoice_type_id,
                "from_id": invoice.from_ids.item_name,
                "to_id": invoice.to_ids.item_name,
                "agent_dovoz_name": agent_dovoz_name,
                "agent_id": invoice.agent.item_name,
                "comment": invoice.comment,
                "delivery": invoice.delivery,
                "quantity": 0,
                "pallet": 0,
                "unit_in_pallet": 0,
                "pkg": 0,
                "unit": 0,
                "weight": 0,
            }
            for body in invoice.invoices_body:
                quantity = body.quantity
                try:
                    pallet = int(quantity / body.goods.amount_inpallet)
                except ZeroDivisionError:
                    pallet = 0
                    print(
                        f"Ошибка: \nНакладная: {invoice.order_number}\n"
                        f"Артикул: {body.goods.marking_goods} - Штук на паллет: {body.goods.amount_inpallet}"
                    )

                unit_in_pallet = pallet * body.goods.amount_inpallet
                qnt = quantity - unit_in_pallet
                try:
                    pkg = int(qnt / body.goods.pieces_pkge)
                except ZeroDivisionError:
                    pkg = 0
                    print(
                        f"Ошибка: \nНакладная: {invoice.order_number}\n"
                        f"Артикул: {body.goods.marking_goods} - Штук в коробе: {body.goods.pieces_pkge}"
                    )
                unit = qnt - (pkg * body.goods.pieces_pkge)
                weight = body.goods.weight * quantity
                inv["quantity"] += quantity
                inv["pallet"] += pallet
                inv["unit_in_pallet"] += unit_in_pallet
                inv["pkg"] += pkg
                inv["unit"] += unit
                inv["weight"] += weight
            data_invoice_detail.append(inv)
        return data_invoice_detail


class InvoiceBodyDao(BaseDao):
    model = InvoiceBody
    url_pg = None

    @staticmethod
    def get_detail_body(invoice_body_list):
        data_body_detail = []
        for invoice in invoice_body_list:
            if invoice.invoice_type_id == 203:
                if invoice.to_ids.dovoz:
                    agent_dovoz_name = invoice.to_ids.dovoz.item_name
                else:
                    agent_dovoz_name = None
            else:
                agent_dovoz_name = "Приход"
            for body in invoice.invoices_body:
                inv = {
                    "acs_number": invoice.acs_number,
                    "order_number": invoice.order_number,
                    "date_doc": invoice.date_doc,
                    "invoice_type_id": invoice.invoice_type_id,
                    "from_id": invoice.from_ids.item_name,
                    "to_id": invoice.to_ids.item_name,
                    "agent_dovoz_name": agent_dovoz_name,
                    "agent_id": invoice.agent.item_name,
                    "comment": invoice.comment,
                    "delivery": invoice.delivery,
                    "marking_goods": body.goods.marking_goods,
                    "goods_id": body.goods_id,
                    "item_name": body.goods.item_name,
                    "pieces_pkge": body.goods.pieces_pkge,
                    "amount_inpallet": body.goods.amount_inpallet,
                    "group_id": body.goods.group_id,
                    "weight": body.goods.weight,
                    "quantity": body.quantity,
                }
                data_body_detail.append(inv)
        return data_body_detail


class AgentDao(BaseDao):
    model = Agent
    filial = None

    @classmethod
    def get(cls, filial: str):
        with session_dict[filial]() as session:
            query = (
                select(cls.model)
                .filter(cls.model.agent_dovoz_id > 0)
                .options(joinedload(cls.model.dovoz))
                .limit(10)
            )
            res = session.execute(query)
            result = res.scalars().all()

    @classmethod
    def get_agent_dovoz(cls, agent_dovoz_id):
        if agent_dovoz_id == 0 or agent_dovoz_id is None:
            return "None"
        with session_dict[cls.filial]() as session:
            query = select(cls.model.item_name).filter_by(id=agent_dovoz_id)
            res = session.execute(query)
            result = res.scalars().all()
            return result[0]


class GoodsDao(BaseDao):
    model = Goods
    url_pg = None

    @classmethod
    def get_group(cls, id_group):
        with session_dict[cls.filial]() as session:
            query = select(cls.model.item_name).filter_by(id=id_group)
            res = session.execute(query)
            result = res.scalars().all()
            return result[0]


if __name__ == "__main__":
    # filter_by = {}
    # AgentDao.get(filial="krd")

    _f = {
        # "acs_number": 11134355
        # "agent_id": 16713245,
        # "program_id": 376,
        # # "delivery": True
    }
    _agent_id = 16713245
    _program_id = 376
    _start_date = "2025-03-01"
    _end_date = "2025-04-01"
    _limit = 10000
    InvoiceDao.filial = "krd"
    result_query = InvoiceDao.get_invoice(
        filter_params=_f,
        start_date=_start_date,
        end_date=_end_date,
        # delivery=True,
        agent_id=_agent_id,
        program_id=_program_id,
        limit=_limit,
    )

    # data = InvoiceBodyDao.get_detail_body(result_query)
    data = InvoiceDao.get_detail_invoice(result_query)
    df = pd.DataFrame(data)
    print(df.to_markdown())
    df.to_excel("inv.xlsx", index=False)
