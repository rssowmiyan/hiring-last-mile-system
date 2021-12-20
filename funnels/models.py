from django.db import models

class DefaultTemplates(models.Model):
    template = models.TextField()

    def __str__(self) -> str:
        return self.template

class Funnel(models.Model):
    funnel_name      = models.CharField(max_length=60)
    segment_name     = models.CharField(max_length=60,default="General")
    sub_segment_name = models.CharField(max_length=60)
    no_of_seq        = models.PositiveSmallIntegerField(default=1)
    start_date       = models.CharField(max_length=20,null=True)

    def __str__(self) -> str:
        return self.funnel_name
    

class Sequence(models.Model):
    funnel_id     = models.ForeignKey('Funnel',on_delete=models.CASCADE,null=True)
    sequence_name = models.CharField(max_length=60)
    description   = models.CharField(max_length=60)
    frequency     = models.PositiveSmallIntegerField(default=3)
    sequence      = models.ForeignKey('DefaultTemplates',on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return self.sequence_name


