from django.contrib import admin
from .models import DefaultTemplates,Sequence,Funnel


class FunnelAdmin(admin.ModelAdmin):
    # list_display = ['funnel_name','segment','sub_segment','no_of_seq','start_date','ongoing','seqs_remaining']
    readonly_fields = ['seqs_remaining',]
admin.site.register(Funnel,FunnelAdmin)
admin.site.register(DefaultTemplates)
admin.site.register(Sequence)

