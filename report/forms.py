import datetime

from dateutil.relativedelta import relativedelta
from django import forms


class PeriodForm(forms.Form):
    today = datetime.date.today()
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "value": today.replace(day=1) - relativedelta(months=1),
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "value": today.replace(day=1),
            }
        )
    )


class FilialForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilialForm, self).__init__(*args, **kwargs)
        self.fields["filial_field"] = forms.ChoiceField(
            widget=forms.Select(
                attrs={"id": "filial_field", "class": "inp_search_file"}
            ),
            label="Филиал",
        )


# creating a form
class ContractsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContractsForm, self).__init__(*args, **kwargs)
        self.fields["contract_field"] = forms.ChoiceField(
            widget=forms.Select(
                attrs={"id": "contract_field", "class": "inp_search_file"}
            ),
            label="Контракт",
        )


class DepartmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields["department_field"] = forms.ChoiceField(
            widget=forms.Select(
                attrs={"id": "department_field", "class": "inp_search_file"}
            ),
            choices=[("sklad", "Склад"), ("tls", "ТЛС")],
            label="Отдел",
        )
