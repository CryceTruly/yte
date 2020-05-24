from django.db import models
from authentication.models import User


class Expense(models.Model):

    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('RENT', 'RENT'),
        ('BUSINESS_MISCELLANEOUS', 'BUSINESS_MISCELLANEOUS'),
        ('TRAVEL', 'TRAVEL'),
        ('GENERAL_MERCHANDISE', 'GENERAL_MERCHANDISE'),
        ('RESTUARANTS', 'RESTUARANTS'),
        ('ENTERTAINMENT', 'ENTERTAINMENT'),
        ('GASOLINE_FUEL', 'GASOLINE_FUEL'),
        ('INSURANCE', 'INSURANCE'),
        ('OTHERS', 'OTHERS')
    ]
    description = models.CharField(max_length=255, db_index=True)
    date = models.DateField(blank=False, null=False)
    description = models.TextField(blank=True)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, blank=False, null=False)
    category = models.CharField(
        max_length=200, choices=CATEGORY_OPTIONS, null=False, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.description
