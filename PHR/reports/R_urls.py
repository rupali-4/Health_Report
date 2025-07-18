from django.urls import path
from . import views

urlpatterns = [
    path('filter_report/', views.report_view, name='n_filter_report'),
]
