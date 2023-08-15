
# Create your models here.
# flipkart_scraper/models.py

from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    reviews = models.PositiveIntegerField()
    ratings = models.DecimalField(max_digits=3, decimal_places=2)
    media_count = models.PositiveIntegerField()

    def __str__(self):
        return self.title
