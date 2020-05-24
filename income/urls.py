from django.urls import path
from .views import IncomesAPIView, IncomeDetailsAPIView


urlpatterns = [
    path('', IncomesAPIView.as_view(), name="incomes"),
    path('<int:id>', IncomeDetailsAPIView.as_view(), name="income")
]
