from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
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
    EARPHONE_TYPE_CHOICES = (
        ('Earbud', 'Earbud'),
        ('Over-Ear', 'Over-Ear'),
        ('On-Ear', 'On-Ear'),
    )
    EARPHONE_FEATURES = (
        ('Wireless', 'Wireless'),
        ('Microphone', 'Microphone'),
        ('Phone-Control', 'Phone-Control')
    )
    earphone_name = models.CharField(null=True, max_length=100)
    brand_name = models.CharField(null=True, max_length=100)
    earphone_type = models.CharField(null=True, max_length=10, choices=EARPHONE_TYPE_CHOICES)
    price = models.PositiveIntegerField()
    earphone_features = ArrayField(
        models.CharField(max_length=20, choices=EARPHONE_FEATURES),
        size=10,
        blank=True,
        default=[],
        help_text='values like Wireless,Microphone,Phone Control...',
    )
    earphone_image = models.ImageField(null=True, upload_to='uploads/earphone_images/')
    pub_date = models.DateTimeField('date published')