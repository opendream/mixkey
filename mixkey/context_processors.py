from django.conf import settings
from domain.models import Project

def site_information(request):
    context = {
        'settings':settings,
        'global_project_list': Project.objects.all().order_by('-created')
    }

    return context