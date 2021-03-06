from django.db import models
from authentication.models import User


class Income(models.Model):

    SOURCES = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE_HUSTLES', 'SIDE_HUSTLES'),
        ('OTHERS', 'OTHERS')
    ]
    date = models.DateField(blank=False, null=False)
    description = models.TextField(blank=True)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, blank=False, null=False)
    source = models.CharField(
        max_length=200, choices=SOURCES, null=False, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.description
