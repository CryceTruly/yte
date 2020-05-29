from django.shortcuts import render
from rest_framework import generics, response, status, views
import datetime
from expenses.models import Expense
from rest_framework import permissions
from income.models import Income
from .renderers import StatsRenderer
# Create your views here.


class ExpenseCategoryStats(views.APIView):
    # categories occuring.
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (StatsRenderer,)

    def get_categories(self, item):
        return item.category

    def get_expense_count(self, y):
        new = Expense.objects.filter(category=y,)
        count = new.count()
        amount = 0
        for y in new:
            amount += y.amount
        return {'count': count, 'amount': amount}

    def get(self, request):
        todays_date = datetime.date.today()
        three_months_ago = datetime.date.today() - datetime.timedelta(days=90)
        expenses = Expense.objects.filter(owner=request.user,
                                          date__gte=three_months_ago, date__lte=todays_date)

        final = {}
        categories = list(set(map(self.get_categories, expenses)))

        for x in expenses:
            for y in categories:
                final[y] = self.get_expense_count(y)
        return response.Response({'category_data': final}, status=status.HTTP_200_OK)


class ExpenseYearlyStats(views.APIView):
    renderer_classes = (StatsRenderer,)

    permission_classes = (permissions.IsAuthenticated,)

    def get_amount_for_month(self, month, all_expenses, today_year):
        month_amount = 0
        for one in all_expenses:
            month_, year = one.date.month, one.date.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    def get(self, request):
        todays_date = datetime.date.today()
        a_year_ago = datetime.date.today() - datetime.timedelta(days=30*12)

        all_expenses = Expense.objects.filter(
            owner=request.user, date__gte=a_year_ago, date__lte=todays_date)
        today = datetime.datetime.today().date()
        today_amount = 0
        months_data = {}
        week_days_data = {}
        for x in range(1, 13):
            today_month, today_year = x, datetime.datetime.today().year
            for one in all_expenses:
                months_data[x] = self.get_amount_for_month(
                    x, all_expenses, today_year)

        return response.Response({'this_year_expenses': months_data}, status=status.HTTP_200_OK)


class IncomeCategoryStats(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (StatsRenderer,)

    def get_sources(self, item):
        return item.source

    def get_sources_count(self, y):
        new = Income.objects.filter(source=y)
        count = new.count()
        amount = 0
        for y in new:
            amount += y.amount
        return {'count': count, 'amount': amount}

    def get(self, request):
        todays_date = datetime.date.today()
        three_months_ago = datetime.date.today() - datetime.timedelta(days=90)
        income = Income.objects.filter(owner=request.user,
                                       date__gte=three_months_ago, date__lte=todays_date)
        final = {}
        sources = list(set(map(self.get_sources, income)))

        for x in income:
            for y in sources:
                final[y] = self.get_sources_count(y)
        return response.Response({'sources_data': final}, status=status.HTTP_200_OK)


class IncomeYearlyStats(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (StatsRenderer,)

    def get_amount_for_month(self, month, all_income, today_year):
        month_amount = 0
        for one in all_income:
            month_, year = one.date.month, one.date.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    def get(self, request):
        todays_date = datetime.date.today()
        a_year_ago = datetime.date.today() - datetime.timedelta(days=30*12)
        all_income = Income.objects.filter(
            owner=request.user, date__gte=a_year_ago, date__lte=todays_date)
        today = datetime.datetime.today().date()
        today_amount = 0
        months_data = {}
        week_days_data = {}

        for x in range(1, 13):
            today_month, today_year = x, datetime.datetime.today().year
            for one in all_income:
                months_data[x] = self.get_amount_for_month(
                    x, all_income, today_year)

        return response.Response({'this_year_income': months_data}, status=status.HTTP_200_OK)
