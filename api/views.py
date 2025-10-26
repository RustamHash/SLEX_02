from rest_framework import generics

from api.serializers import FilialSerializer
from base_app.models import Filial, Contracts


class FilialsAPIView(generics.ListAPIView):
    queryset = Filial.objects.filter(as_active=True)
    serializer_class = FilialSerializer
