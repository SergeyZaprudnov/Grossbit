from django.urls import path

from cash_machine.views import cashe_machine

urlpatterns = [
    path('cashe_machine', cashe_machine, name='cash_machine'),
]
