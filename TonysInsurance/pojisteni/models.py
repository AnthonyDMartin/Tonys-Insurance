from django.db import models
from django.contrib.auth.models import User
from pojistenec.models import Customer


class Category(models.Model):
    category_name = models.CharField(max_length=20)
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.category_name


class Policy(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    policy_name = models.CharField(max_length=200)
    sum_assurance = models.PositiveIntegerField()
    premium = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField()
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.policy_name


class PolicyRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='Čeká na schválení')
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.customer


class Question(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    admin_comment = models.CharField(max_length=200, default='')
    asked_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.description
