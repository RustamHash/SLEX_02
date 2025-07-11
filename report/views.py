from django.http import FileResponse
from django.shortcuts import render

from report.forms import ContractsForm, FilialForm, PeriodForm, DepartmentForm
from report.models import Reports
from report.utils.billing_utils import billing as billing_utils


def index(request):
    context = {"reports": Reports.objects.filter(as_active=True)}
    return render(request, "report/reports.html", context=context)


def billing(request, **kwargs):
    context = {
        "reports": Reports.objects.filter(as_active=True),
        "form_contracts": ContractsForm(),
        "form_filials": FilialForm(),
        "form_periods": PeriodForm(),
        "form_department": DepartmentForm(),
    }
    if request.method == "POST":
        kwargs = request.POST.dict()
        file_ = billing_utils(**kwargs)
        return FileResponse(open(file_, "rb"))
    return render(request, "report/billing.html", context=context)
