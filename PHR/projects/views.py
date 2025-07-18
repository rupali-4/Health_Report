from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required
from .forms import CreateProjectForm, VertexAllocationForm
from django.http import HttpResponseForbidden
from .models import CreateProject, VertexAllocation
from allocation.models import VpRmAllocation
from batches.models import CreateBatch


VERTEX_LIST = ['Diya', 'Deep Tech', 'SAVE', 'BEST']

@login_required    # Ensures only logged-in users can access this view
def create_project(request):
  # Correct condition — only allow 'pmo' role
  if request.user.role != 'pmo':
    return HttpResponseForbidden("You are not authorized to access this page.")

  # if form is submitted
  if request.method == 'POST':
    form = CreateProjectForm(request.POST)
    allocation_forms = []    # We'll manually build one allocation form for each vertex

    valid = form.is_valid()   # Track if all forms are valid
    total_allocated = 0       # Track total of all vertex targets

    # Build one allocation form per vertex manually: Loop through each fixed vertex to build its form
    for vertex in VERTEX_LIST:
      # Create form data with fixed vertex + its target from POST data
      form_data = {
        'vertex': vertex,  # fixed vertex
        'target': request.POST.get(f'target_{vertex}', 0)  # dynamic field name like target_Diya
      }
      vertex_form = VertexAllocationForm(form_data)
      allocation_forms.append(vertex_form)

      # Check if individual allocation form is valid: include its target in total
      if vertex_form.is_valid():
        total_allocated += int(vertex_form.cleaned_data['target'])
      else:
        valid = False   # If any form fails validation, mark entire process as invalid

    if valid:     # If both project form and all allocation forms are valid
      total_target = form.cleaned_data['total_target']

      # Check if total matches allocated targets match project's total target
      if total_allocated != total_target:
        error_msg = f"Total allocated ({total_allocated}) must equal total target ({total_target})."
        return render(request, 'create_project.html', {
            'form': form,
            'allocation_forms': allocation_forms,
            'error': error_msg  # shown in template
        }) 

      # Save the project
      project = form.save(commit=False)   # not Save to DB
      project.created_by = request.user   # Add the logged-in user as creator
      project.save()    # Save to DB

      # Save each vertex allocation
      for vertex_form in allocation_forms:
        allocation = vertex_form.save(commit=False)
        allocation.project = project
        allocation.save()

      return redirect('n_projectlist')   # once project created is saved, go to project list page
    else:
      print("Project form errors:", form.errors)  # ✅ Debug line
  else:     # If GET request, create blank forms
    form = CreateProjectForm()
    allocation_forms = [
      VertexAllocationForm(initial={'vertex': v}) for v in VERTEX_LIST
    ]     # Each form pre-filled with vertex name

  return render(request, 'create_project.html', {
    'form': form,
    'allocation_forms': allocation_forms,
  })    # Render the template with forms


from django.shortcuts import get_object_or_404
@login_required
def project_details(request, pk):  # Accept pk from URL (proj id assign h url me isliye pk add karn pada)
    project = get_object_or_404(CreateProject, pk=pk)
    user = request.user
    allocations = []
    quarter_allocations = []
    vertex_allocations = []

    if user.role == 'vp':
        allocations = VpRmAllocation.objects.filter(project=project)

    elif user.role == 'rm':
        allocations = VpRmAllocation.objects.filter(project=project, rm_user=user)
        
    elif user.role == 'pmo':
        vertex_allocations = VertexAllocation.objects.filter(project=project)

    elif user.role == 'cm':
      try:
            assigned_center = AssignCenter.objects.get(cm_user=user)
            quarter_allocations = RmCenterQuarterAllocation.objects.filter(
            project=project,
            center=assigned_center
          )
      except AssignCenter.DoesNotExist:
            quarter_allocations = []

    else:
        allocations = []

    return render(request, 'project_details.html', {
        'project': project, 'vertex_allocations': vertex_allocations,
        'allocations': allocations, 'quarter_allocations': quarter_allocations
    })


from allocation.models import VpRmAllocation, RmCenterQuarterAllocation
from batches.models import CreateBatch, AssignCenter

@login_required
def project_list(request):
  user = request.user

  if user.role == 'pmo' or user.role == 'vp':
    projects = CreateProject.objects.all()

  elif user.role == 'rm':
    # Projects assigned to this RM by VP
    rm_allocations = VpRmAllocation.objects.filter(rm_user=user)
    projects = CreateProject.objects.filter(id__in=rm_allocations.values('project'))

  elif user.role == 'cm':
    try:
        center_obj = AssignCenter.objects.get(cm_user=user)
        allocated_projects = RmCenterQuarterAllocation.objects.filter(
            center=center_obj
        ).values_list('project', flat=True).distinct()
        projects = CreateProject.objects.filter(id__in=allocated_projects)
    except AssignCenter.DoesNotExist:
        projects = []
  else:
    projects = []  # no projects for other roles

  return render(request, 'project_list.html', {'projects': projects})
