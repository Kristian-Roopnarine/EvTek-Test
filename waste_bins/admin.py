from django.contrib import admin
from .models import PickUp,Notes,WasteBinType
# Register your models here.

admin.site.register(PickUp)
admin.site.register(Notes)
admin.site.register(WasteBinType)