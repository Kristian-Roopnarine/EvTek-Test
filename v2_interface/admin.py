from django.contrib import admin
from .models import NotesV2,PickUpV2,WasteBinTypeV2,ConfirmPickUp,PickUpReminder
# Register your models here.

admin.site.register(NotesV2)
admin.site.register(PickUpV2)
admin.site.register(WasteBinTypeV2)
admin.site.register(ConfirmPickUp)
admin.site.register(PickUpReminder)
