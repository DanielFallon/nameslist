from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Prospective(models.Model):
    id = models.AutoField(primary_key=True)


class Name(models.Model):
    prospective_id = models.ForeignKey(Prospective)
    user_id = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=256)
    correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('prospective_id', 'user_id',)


class Photo(models.Model):
    prospective_id = models.ForeignKey(Prospective)
    user_id = models.ForeignKey(User)
    url = models.TextField()
    primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('prospective_id', 'user_id',)


class Fact_Type(models.Model):
    sortorder = models.PositiveIntegerField(unique=True)
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=256)
    TEXT = 0
    BLOB = 1
    PROMPT_TYPE_CHOICES = (
        (TEXT, 'text'),
        (BLOB, 'blob')
    )
    prompt_type = models.SmallIntegerField(choices=PROMPT_TYPE_CHOICES)
    question = models.TextField()


class Fact(models.Model):
    fact_type_id = models.ForeignKey(Fact_Type)
    user_id = models.ForeignKey(User, null=True, blank=True)
    prospective_id = models.ForeignKey(Prospective)
    fact = models.CharField(max_length=256)

    class Meta:
        unique_together = ('fact_type_id', 'user_id', 'prospective_id',)


class Opinion_Prompt(models.Model):
    sortorder = models.PositiveIntegerField(unique=True)
    prompt_text = models.TextField()


class Opinion(models.Model):
    opinion_prompt_id = models.ForeignKey(Opinion_Prompt)
    user_id = models.ForeignKey(User)
    prospective_id = models.ForeignKey(Prospective)
    opinion = models.TextField()

    class Meta:
        unique_together = ('opinion_prompt_id', 'user_id', 'prospective_id',)
