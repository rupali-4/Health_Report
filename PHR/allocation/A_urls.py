from django.urls import path
from . import views

urlpatterns = [
    path('vp-allocates/', views.vp_allocates_rm, name="n_vp_allocates"),
    path('rm-allocates/', views.rm_allocates_center, name="n_rm_allocates"),
]
