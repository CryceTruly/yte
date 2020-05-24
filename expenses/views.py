from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import ExpenseSerializer
from .models import Expense
from .permissions import IsOwner
from .renderers import ExpenseRenderer
# Create your views here.


class ExpenseListView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (ExpenseRenderer,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    renderer_classes = (ExpenseRenderer,)

    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
