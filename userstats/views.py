from django.shortcuts import render
from rest_framework import generics, response, status, views
# Create your views here.


class ExpenseCategoryStats(views.APIView):
    def get(self, request):
        return response.Response({'category_data': []}, status=status.HTTP_200_OK)


class ExpenseYearlyStats(views.APIView):
    def get(self, request):
        return response.Response({'this_year_expenses': []}, status=status.HTTP_200_OK)


class IncomeCategoryStats(views.APIView):
    def get(self, request):
        return response.Response({'sources_data': []}, status=status.HTTP_200_OK)


class InconeYearlyStats(views.APIView):
    def get(self, request):
        return response.Response({'this_year_income': []}, status=status.HTTP_200_OK)
