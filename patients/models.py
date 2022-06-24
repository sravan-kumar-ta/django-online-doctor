from django.db import models

from accounts.models import CustomUser


class FamilyMembers(models.Model):
    relation_with = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    relation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
