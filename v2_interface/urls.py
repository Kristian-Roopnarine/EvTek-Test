from django.urls import path
from . import views

app_name="v2_interface"

urlpatterns = [
    path('',views.index,name='home'),
    path('schedule/list/',views.CalendarView.as_view(),name="schedule-list")
]