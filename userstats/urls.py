from django.urls import path
from .views import ExpenseCategoryStats, IncomeCategoryStats, ExpenseYearlyStats, IncomeCategoryStats, IncomeYearlyStats

urlpatterns = [
    path('expense_category_data', ExpenseCategoryStats.as_view(),
         name="expense_category_data"),
    path('income_sources_data', IncomeCategoryStats.as_view(),
         name="income_sources_data"),
    path('this_year_expenses', ExpenseYearlyStats.as_view(),
         name="this_year_expenses"),
    path('this_year_income', IncomeYearlyStats.as_view(),
         name="this_year_income"),
]
