from django.db import models
from django.contrib.auth.models import AbstractUser

TRANSACTION_TYPE_CHOICES = [
    ('grant', 'Grant'),
    ('redeem', 'Redeem')
]

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_name = models.CharField(max_length=100, blank=False)
    points = models.DecimalField(max_digits=29, decimal_places=10, default=0)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=29, decimal_places=10, default=0)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)