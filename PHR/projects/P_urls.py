from django.urls import path
from . import views

# aboove: no need here but to run code to see home html page i added this here
# if ntg is in urls file it show error hence added this for now

urlpatterns = [
    path('createproject/', views.create_project, name= 'n_createproject'),
    path('projectdetails/<int:pk>/', views.project_details, name= 'n_projectdetails'),
    path('projectlist/', views.project_list, name= 'n_projectlist'),
]
