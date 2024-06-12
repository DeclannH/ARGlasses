from django.urls import path
from .views import update_repair_status_and_steps, repair_form

urlpatterns = [
    path('repair/<str:repair_id>/', update_repair_status_and_steps, name='update_repair'),
    path('repair_form/<str:repair_id>/', repair_form, name='repair_form'),
]
