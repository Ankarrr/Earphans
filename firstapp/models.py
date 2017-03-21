from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        return timezone.now() > self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ForeignKey: you will automagically get the inverse relation on instances of the question model back to the set of possible choices.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Earphone(models.Model):
    earphone_name = models.CharField(null=True, max_length=100)
    brand_name = models.CharField(null=True, max_length=100)
    earphone_description = models.CharField(null=True, max_length=1000)
    price = models.PositiveIntegerField()
    earphone_image = models.ImageField(null=True, upload_to='static/fistapp/images/earphones')
    pub_date = models.DateTimeField('date published')