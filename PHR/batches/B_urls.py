from django.urls import path
from . import views


urlpatterns = [
    path('assign-region/', views.assign_region_to_rm, name="n_assign_region"),
    path('assign-center/', views.assign_center_to_cm, name="n_assign_center"),
    path('create-batch/', views.create_batch, name="n_create_batch"),
    path('enroll-student/', views.enroll_student, name="n_enroll_student"),
    path('batchdetails/<int:pk>/', views.batch_details, name= 'n_batchdetails'),
    path('batchlist/', views.batch_list, name= 'n_batchlist'),
    
]

# here i will add code for vp to assign regions to available rms
# rm to assign centers & cm under them
# cm to assign batches under them 
