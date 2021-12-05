from django.db import models

class DefaultTemplates(models.Model):
    template = models.TextField()

    def __str__(self) -> str:
        return self.template

class Funnel(models.Model):
    funnel_name      = models.CharField(max_length=60)
    segment_name     = models.CharField(max_length=60,default="General")
    sub_segment_name = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.funnel_name
    

class Sequence(models.Model):
    sequence_name = models.CharField(max_length=60)
    description   = models.CharField(max_length=60)
    frequency     = models.PositiveSmallIntegerField()
    sequence      = models.ForeignKey('DefaultTemplates',on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return self.sequence_name


