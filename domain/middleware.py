from django.shortcuts import redirect
from django.utils.translation import activate     
from django.conf import settings

from domain.models import Project

import re

class ForceInEnglish(object):

    def process_request(self, request):   
        if re.match(".*admin/", request.path):          
            activate("en")      
            

class ProjectMiddleware(object):
    
    project_code = ''
    project_selected = None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        # ignore case
        if request.path.split('/')[1] in ['api', 'c', 'admin', 'language']:
            return None
        
        project_code = view_kwargs.get('project_code') or ''
        self.project_code = project_code
        
        if self.project_code.lower() == 'all':
            self.project_selected = None
            return
        
        try:
            if project_code:
                self.project_selected = Project.objects.get(code__iexact=project_code.lower())
        except Project.DoesNotExist:
            pass
        
        if not self.project_selected:
            project_code = request.COOKIES.get('project_selected')
            try:
                if project_code:
                    self.project_selected = Project.objects.get(code__iexact=project_code.lower())
                    
            except Project.DoesNotExist:
                pass
        
        request.META['PROJECT_SELECTED'] = self.project_selected
        
        
        # Redirect to project selected page
        if self.project_code.lower() == 'all':
            request.META['PROJECT_SELECTED'] = None
        elif not self.project_code and self.project_selected:
            return redirect('project_overview', project_code=self.project_selected.code.lower())
                
        
        return None
        
    def process_response(self, request, response):
        
        
        if self.project_code.lower() == 'all':
            #response = redirect('home')
            response.set_cookie('project_selected', 'all')
            
        elif self.project_selected:
            response.set_cookie('project_selected', self.project_selected.code.lower())            

        return response
        
