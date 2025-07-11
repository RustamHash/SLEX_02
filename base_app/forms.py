from django import forms


# contracts_all = Contracts.objects.all()


def append_contract_choices(contracts_all):
    contract_choice = []
    for contract in contracts_all:
        _ = (contract.id, contract.name)
        contract_choice.append(_)
    return contract_choice


# creating a form
class SverkiForm(forms.Form):
    def __init__(self, choice_contracts, *args, **kwargs):
        self.choice_contracts = choice_contracts
        super(SverkiForm, self).__init__(*args, **kwargs)
        self.fields["contract_field"].widget.attrs["class"] = "contract_field"
        self.fields["contract_field"] = forms.ChoiceField(
            choices=append_contract_choices(contracts_all=self.choice_contracts),
            label="Контракты",
        )
