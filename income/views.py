from rest_framework import generics, status
from rest_framework.response import Response
from .models import Income
from .serializers import IncomeSerializer
from rest_framework import permissions
from .permissions import IsOwner
from .renderers import IncomeJSONRenderer


class IncomesAPIView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    renderer_classes = (IncomeJSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    renderer_classes = (IncomeJSONRenderer,)
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)
