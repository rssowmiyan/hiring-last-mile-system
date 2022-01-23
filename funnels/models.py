from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.conf import settings


class DefaultTemplates(models.Model):
    template = models.TextField()

    def __str__(self) -> str:
        return self.template

class Funnel(models.Model):
    CHOICES = (
        ('D', 'Draft'),
        ('O', 'Ongoing'),
        ('C', 'Completed'),
    )
    created_by       = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      on_delete=models.CASCADE,
      null=True,
      blank=True
    )
    funnel_name      = models.CharField(max_length=60)
    segment          = models.CharField(max_length=60,default="General")
    sub_segment      = models.CharField(max_length=60,blank=True)
    no_of_seq        = models.PositiveSmallIntegerField(default=1)
    start_date       = models.DateField(null=True)
    status           = models.CharField(max_length=20,choices=CHOICES,default='D')
    seqs_remaining   = models.PositiveSmallIntegerField(default=1)


    # def __str__(self) -> str:
    #     return self.funnel_name
    

class Sequence(models.Model):
    funnel_id     = models.ForeignKey('Funnel',on_delete=models.CASCADE,null=True)
    sequence_name = models.CharField(max_length=60)
    description   = models.CharField(max_length=60)
    frequency     = models.PositiveSmallIntegerField(default=3,validators=[MinValueValidator(3)])
    sequence      = models.ForeignKey('DefaultTemplates',on_delete=models.CASCADE,null=True)
    sch_date      = models.DateField(null=True)

    def __str__(self) -> str:
        return self.sequence_name


