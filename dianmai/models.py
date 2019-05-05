from django.db import models

# Create your models here.
class SecuritiesManager(models.Manager):
    pass

class Security(models.Model):
    id = models.AutoField(primary_key=True)
    securityName = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
