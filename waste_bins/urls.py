from django.urls import path,include
from . import views

app_name ="waste_bins"

urlpatterns = [
    path('',views.index,name="home"),
    path('schedule/list/',views.PickUpList.as_view(),name="schedule-list"),
    path('schedule/create-pick-up/',views.PickUpCreateForm.as_view(),name="create-pick-up"),
    path('schedule/edit-pick-up/<int:pk>/',views.PickUpUpdateForm.as_view(),name="edit-pick-up"),
    path('schedule/delete-pick-up/<int:pk>/',views.PickUpDeleteForm.as_view(),name='delete-pick-up'),


    path('dashboard/',views.dashboard,name="dashboard"),
    path('dashboard/bin-pickup-dates/<str:bin_type_name>/',views.BinPickUpDates.as_view(),name="dashboard-pickup-dates")
]