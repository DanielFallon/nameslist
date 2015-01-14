from functools import lru_cache
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.utils.functional import cached_property


class Prospective(models.Model):
    id = models.AutoField(primary_key=True)

    @cached_property
    def name(self):
        return self.name_list[0]

    @cached_property
    def name_list(self):
        return self.name_set.extra(order_by = ['-correct','-id'])

    @cached_property
    def photo(self):
        return self.photo_list[0]

    @cached_property
    def photo_list(self):
        return  self.photo_set.extra(order_by = ['-primary','-id'])


    def fact(self,fact_id):
        return self.fact_list(fact_id)[0]

    @lru_cache()
    def fact_list(self,fact_id):
        return self.fact_set.all().filter(fact_type_id_id=fact_id).extra(order_by = ['-id'])

    @cached_property
    def get_all_opinions(self):
        opinion_sets = {}
        all_opinions = self.opinion_set.all()
        for opinion in all_opinions:
            if opinion_sets[opinion.opinion_prompt_id_id]:
                opinion_sets[opinion.opinion_prompt_id_id].append(opinion)
            else:
                opinion_sets[opinion.opinion_prompt_id_id] = []
        opinion_prompts = Opinion_Prompt.objects.all().extra(order_by = ['sortorder'])
        return [(opinion_prompt,opinion_sets.get(opinion_prompt.id)) for opinion_prompt in opinion_prompts]

    @cached_property
    def facts(self):
        fact_sets = {}
        all_facts = self.fact_set.all()
        for fact in all_facts:
            if fact_sets[fact.fact_type_id_id]:
                fact_sets[fact.fact_type_id_id].append(fact)
            else:
                fact_sets[fact.fact_type_id_id] = []
        fact_types = Fact_Type.objects.all().extra(order_by = ['sortorder'])
        return [(fact_type,fact_sets.get(fact_type.id)) for fact_type in fact_types]



class Name(models.Model):
    prospective_id = models.ForeignKey(Prospective)
    user_id = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=256)
    correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('prospective_id', 'user_id',)

    def __str__(self):
        return "%d: %s"%(self.prospective_id_id,self.name)

class Photo(models.Model):
    prospective_id = models.ForeignKey(Prospective)
    user_id = models.ForeignKey(User)
    url = models.TextField()
    primary = models.BooleanField(default=False)

    def to_json(self):
        return {'prospective_id': self.prospective_id_id,
                'user_id': self.user_id.first_name + " " + self.user_id.last_name,
                'url': self.url,
                'primary': self.primary,
                }

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
