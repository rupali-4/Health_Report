from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from batches.models import CreateBatch, Enrollment, AssignCenter, CENTER_CHOICES
from projects.models import CreateProject
from allocation.models import RmCenterQuarterAllocation
import csv
import io
from xhtml2pdf import pisa


@login_required
def report_view(request):
    # Fetch filters from GET params
    #project_id = request.GET.get('project')   # 'project' is not the model name, It's the name of the query parameter coming from the URL, ex: http://yourdomain.com/reports/?project=3
    #quarter = request.GET.get('quarter')
    #center_id = request.GET.get('center')
    #vertex = request.GET.get('vertex')
    export_type = request.GET.get('export')  # csv or pdf
    
    project_id = request.GET.get('project')
    quarter = request.GET.get('quarter', '').strip()
    center_id = request.GET.get('center', '').strip()
    vertex = request.GET.get('vertex', '').strip()
    
    # Base queryset
    batches = CreateBatch.objects.all()

    # Apply filters if provided
    if project_id:
        batches = batches.filter(project_id=int(project_id))  # convert to int
    if quarter:
        batches = batches.filter(quarter=quarter.strip())     # string is fine, but ensure no spaces
    if center_id:
        batches = batches.filter(center=center_id.strip())    # center is a choice field, stored as string
    if vertex:
        batches = batches.filter(vertex=vertex.strip())       # also a string
        
 
    # Calculate summary data for table: Target vs Achievement
    data = []
    for batch in batches:
        enroll_count = Enrollment.objects.filter(batch=batch).count()
        data.append({
            'project': batch.project.name,
            'center': batch.get_center_display(),
            'batch': batch.name,
            'quarter': batch.quarter,
            'vertex': batch.vertex,
            'target': batch.target,
            'achieved': enroll_count,
        })

    # CSV Export
    if export_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="target_vs_achievement.csv"'

        writer = csv.writer(response)
        writer.writerow(['Project', 'Center', 'Batch', 'Quarter', 'Vertex', 'Target', 'Achieved'])
        for row in data:
            writer.writerow([row['project'], row['center'], row['batch'], row['quarter'], row['vertex'], row['target'], row['achieved']])
        return response

    # PDF Export
    if export_type == 'pdf':
        template = render_to_string('pdf_template.html', {'data': data})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="target_vs_achievement.pdf"'
        pisa.CreatePDF(io.BytesIO(template.encode('utf-8')), dest=response)
        return response

    # Normal HTML page rendering
    context = {
        'data': data,
        'projects': CreateProject.objects.all(),
        'centers': CENTER_CHOICES,
        'quarters': ['Q1', 'Q2', 'Q3', 'Q4'],
        'vertices': ['Diya', 'SAVE', 'Deep Tech', 'BEST']
    }

    return render(request, 'targetachieve.html', context)
