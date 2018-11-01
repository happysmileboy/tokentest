from django.db import models

# Create your models here.

class Account(models.Model):
    address = models.TextField(verbose_name="주소")


class Contract(models.Model):
    address = models.TextField(verbose_name="주소")
    creator = models.TextField(verbose_name="생성자")
    abi = models.TextField(verbose_name="abi")
