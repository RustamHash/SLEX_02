import pandas as pd

from base_app.models import Filial, Contracts
from report.pg_orm.dao import InvoiceDao
from report.utils.utils import save_reports_stock_to_excel


# InvoiceDao принимает

# filter_params=_f,
# start_date=_start_date,
# end_date=_end_date,
# delivery=True,
# agent_id=_agent_id,
# program_id=_program_id,
# limit=_limit,


def billing(**kwargs):
    department = kwargs["department_field"]
    # if department == "tls":
    file_name = billing_tls(**kwargs)
    return file_name


def billing_tls(**kwargs):
    filial = Filial.objects.get(slug=kwargs["filial_field"])
    contract = Contracts.objects.get(slug=kwargs["contract_field"])
    start_date = kwargs["start_date"]
    end_date = kwargs["end_date"]
    department = kwargs["department_field"]
    InvoiceDao.filial = filial.slug
    _limit = 10000
    if department == "tls":
        delivery = True
    else:
        delivery = None
    invoices = InvoiceDao.get_detail_invoice(
        start_date=start_date,
        end_date=end_date,
        delivery=delivery,
        agent_id=contract.id_agent,
        program_id=filial.prog_id,
        limit=_limit,
    )
    df = pd.DataFrame(invoices)
    file_name = save_reports_stock_to_excel(
        _contract=contract, _df_stocks_save=df, _type_reports="Биллинг"
    )
    return file_name
