from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    role = models.CharField(max_length=1, blank=False, null=False, default="p")
    treatedBy = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    history = models.CharField(max_length=1000, blank=True, null=True)
    img = models.ImageField(blank=True, null=True)
    diagnosis = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    sex = models.CharField(max_length=1, blank=False, null=False)

    def __str__(self):
        if f'{self.first_name} {self.last_name}' != ' ':
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'