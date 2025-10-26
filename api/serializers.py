from rest_framework import serializers

from base_app.models import Filial, Contracts


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contracts
        fields = "__all__"


class FilialSerializer(serializers.ModelSerializer):
    contracts = ContractSerializer(many=True)

    class Meta:
        model = Filial
        fields = "__all__"
