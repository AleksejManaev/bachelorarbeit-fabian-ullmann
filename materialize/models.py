from django.db import models

# Create your models here.

class MaterializeForeignModel(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)


class MaterializeTestModel(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    message = models.TextField(max_length=1000)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    file = models.FileField(null=True, blank=True)
    foreign = models.ForeignKey(MaterializeForeignModel, null=True, blank=True)
