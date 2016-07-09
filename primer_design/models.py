from django.db import models

# Create your models here.
from django import forms


class Primer(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    sequen = models.FileField(upload_to='media/hla')
    rangelength = models.IntegerField(default=1000, blank=True)
    maxnumber = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class PrimerForm(forms.ModelForm):
    class Meta:
        models = Primer
        fields = '__all__'
