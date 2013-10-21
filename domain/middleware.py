from domain.models import Project

class ProjectMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        project_code = view_kwargs.get('project_code')
        
        project_selected = False
        try:
            if project_code:
                project_selected = Project.objects.get(code__iexact=project_code.lower())
        except IndexError:
            pass
        except Project.DoesNotExist:
            pass
        
        request.META['PROJECT_SELECTED'] = project_selected
            
        return None