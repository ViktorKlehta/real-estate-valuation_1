from django.contrib import admin
from .models import RealEstate


class EstateModelAdmin (admin.ModelAdmin):
    list_display = ['id', 'type', 'room_count', 'total_area', 'street', 'floor']
    class Meta:
        model=RealEstate

admin.site.register(RealEstate, EstateModelAdmin)