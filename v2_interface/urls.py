from django.urls import path
from . import views

app_name="v2_interface"

urlpatterns = [
    path('',views.index,name='home'),
    path('schedule/list/',views.CalendarView.as_view(),name="schedule-list"),

    path('schedule/list/pickup/<int:pk>/',views.PickUpDetailView.as_view(),name='pickup-detail'),
    path('schedule/list/pickup/delete/<int:pk>/',views.PickUpDeleteView.as_view(),name='delete-pickup'),
    path('schedule/list/pickup/edit/<int:pk>/',views.PickUpEditView.as_view(),name='edit-pickup'),
    path('schedule/list/pickup/create/',views.PickUpCreateView.as_view(),name='create-pickup'),

    #path('dashboard/',views.dashboard,name="dashboard"),
    path('dashboard/bin-pickup-dates/<int:pk>/',views.BinPickUpDates.as_view(),name="dashboard-pickup-dates"),
    path('bin_data/',views.bin_pound_data)

]