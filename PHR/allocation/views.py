from django.shortcuts import render, redirect
from .models import VpRmAllocation, RmCenterQuarterAllocation
# Create your views here.
from .forms import VpRmAllocationForm, RmCenterQuarterForm

# VP assigns vertex target to RMs
def vp_allocates_rm(request):
    if request.method == 'POST':
        form = VpRmAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('n_vp_allocates') 
    else:
        form = VpRmAllocationForm()
    
    all_allocations  = VpRmAllocation.objects.all()
    has_allocations = all_allocations .exists()
    

    return render(request, 'vp.html', {
        'vpform': form,
        'region_assign': all_allocations ,
        'has_allocations': has_allocations,
    })


# RM assigns quarter-wise target to centers
def rm_allocates_center(request):
    if request.method == 'POST':
        form = RmCenterQuarterForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.rm_user = request.user 
            allocation.save()
            return redirect('n_rm_allocates')
    else:
        form = RmCenterQuarterForm()

    my_allocations = RmCenterQuarterAllocation.objects.filter(rm_user=request.user)
    has_allocations = my_allocations.exists()

    return render(request, 'rm.html', {
        'rmform': form,
        'center_assign': my_allocations,
        'has_allocations': has_allocations,
    })
    