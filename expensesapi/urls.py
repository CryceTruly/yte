"""expensesapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="EXPENSE INCOME API",
        default_version='v1',
        description="My Expenses Income API",
        terms_of_service="https://www.co.com/policies/terms/",
        contact=openapi.Contact(email="contact@expense.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
    path('auth/', include(('authentication.urls',
                           'authentication'), namespace="authentication")),

    path('expenses/', include(('expenses.urls',
                               'expenses'), namespace="expenses")),
    path('income/', include(('income.urls',
                             'income'), namespace="income")),
    path('userstats/', include(('userstats.urls',
                                'userstats'), namespace="userstats")),
]
