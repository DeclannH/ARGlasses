from django.urls import path
from .views import update_repair_status_and_steps

urlspatterns = [
    path('repair/<str:repair_id>/', update_repair_status_and_steps, name='update_repair'),
]