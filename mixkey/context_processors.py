from django.conf import settings
from django.shortcuts import get_object_or_404

from domain.models import Project

def site_information(request):
            
    context = {
        'settings':settings,
        'global_project_list': Project.objects.all().order_by('-created'),
        'project_selected': request.META['PROJECT_SELECTED'],
    }

    return context