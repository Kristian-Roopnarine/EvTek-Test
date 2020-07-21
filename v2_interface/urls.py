from django.urls import path
from . import views

app_name="v2_interface"

urlpatterns = [
    path('',views.index,name='home'),
    path('calendar/',views.CalendarView.as_view(),name="calendar")
]