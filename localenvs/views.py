import json
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from localenvs.models import Environments #model import
from localenvs.models import Project
from localenvs.modules.manageenv import Createenv
from localenvs.modules.manageenv import Removeenv
from localenvs.modules.backupenv import Backupenv
from localenvs.modules.gitenv import Gitenv

from localenvs.form import DashboardForm

def index(request):
    return HttpResponse("index")

def dashboard(request):
    
    if request.user.is_authenticated():
        template = 'frontend/dashboard.html'
        
        projects = Project.objects.all()
        array = {}
        
        for project in projects:
            key = str(project.name)
            value = Environments.objects.filter(project=project.id)
            array[key] = value
                    
        return render_to_response(template, {'envs':sorted(array.iteritems()) }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/localenvs/')
    
def formresolution(request):
    
    template = 'frontend/dashboard.html'

    if request.method == 'POST': # If the form has been submitted...
        form = DashboardForm(request.POST) # A form bound to the POST data    
        if form.is_valid(): # All validation rules pass
            
            envName = form.cleaned_data['env_name'] # for getting separated values from the form
            envPath = '/home/html/ecomwiseenvs/' + form.cleaned_data['env_radio'] + '/' + form.cleaned_data['env_path'] + '/'
            envDomain = 'www.' + form.cleaned_data['env_domain'] + '.' + form.cleaned_data['env_radio'] + '.com'
            envDbname = 'dev_' + form.cleaned_data['env_radio'] + '_' + form.cleaned_data['env_dbname']
            envProject = form.cleaned_data['env_radio']
            
            if ( form.cleaned_data['env_radio'] == 'ecomwisedev' ):
                envRadio = 1
            elif ( form.cleaned_data['env_radio'] == 'malibudev' ):
                envRadio = 2
            elif ( form.cleaned_data['env_radio'] == 'etailmindsdev' ):
                envRadio = 3
            else:
                envRadio = 1

            createenv = Createenv()
            createenvSuccess, createenvMessage = createenv.index(envProject, envName, envPath, envDomain, envDbname)
            
            if createenvSuccess is True:
                projectId = Project.objects.get(id=envRadio)
                
                dbInsert = Environments(name = envName, path = envPath, domain = envDomain, dbname = envDbname, project = projectId)
                dbInsert.save()
                
                template = 'frontend/submitform.html'
                returnPage = 'dashboard'
                returnText = "Insert successfull"
                
                return render_to_response(template, {'returnText': returnText, 'returnPage' : returnPage, 'returnMessage': createenvMessage})
            else:
                template = 'frontend/submitform.html'
                returnPage = 'dashboard'
                returnText = "Insert failed"
                
                return render_to_response(template, {'returnText': returnText, 'returnPage' : returnPage, 'returnMessage': createenvMessage})
            
        else:
            return HttpResponse("form is not valid")
    else:
        form = DashboardForm() # An unbound form
        return HttpResponse("import failed")
        
def removeenv(request):
    
    if request.is_ajax():
        envName = request.POST['envname']
          
        envsFiletr = Environments.objects.filter(name=envName)    
        for columns in envsFiletr:
            envId = columns.id
            envPath = columns.path
            envDomain = columns.domain
            envDbname = columns.dbname
            envProjectid = columns.project_id
            
        projects = Project.objects.filter(id=envProjectid)
        for columns in projects:
            envProject = columns.name
        
        removeenv = Removeenv()
        removeenvSuccess, removeenvMessage = removeenv.index(envProject, envName, envPath, envDomain, envDbname)
        
        if removeenvSuccess is True:
            envsAll = Environments.objects.get(id=envId)
            envsAll.delete()
            
            template = 'frontend/submitform.html'
            returnPage = 'dashboard'
            returnText = "Successfull removing"
            
            response_data = {}
            response_data['success'] = removeenvSuccess
            response_data['message'] = removeenvMessage
                    
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else: 
            template = 'frontend/submitform.html'
            returnPage = 'dashboard'
            returnText = "Remove failed"
            
            response_data = {}
            response_data['success'] = removeenvSuccess
            response_data['message'] = removeenvMessage
                    
            return HttpResponse(json.dumps(response_data), content_type="application/json")

def gitenv(request):
    
    if request.is_ajax():
        
        envName = request.POST['envname']
        gitOption = request.POST['gitoption']
        
        envsFiletr = Environments.objects.filter(name=envName)    
        for columns in envsFiletr:
            envId = columns.id
            envPath = columns.path
            envDomain = columns.domain
            envDbname = columns.dbname
            envProjectid = columns.project_id
                
        projects = Project.objects.filter(id=envProjectid)
        for columns in projects:
            envProject = columns.name
        
        gitenv = Gitenv()
        gitOutput = gitenv.index(gitOption, envName, envPath, envProject)
            
        return HttpResponse(json.dumps(gitOutput), content_type="application/json")
        
def backupenv(request):
     
    if request.is_ajax():
        
        envName = request.POST['envname']
        envsFiletr = Environments.objects.filter(name=envName)    
        for columns in envsFiletr:
            envId = columns.id
            envPath = columns.path
            envDomain = columns.domain
            envDbname = columns.dbname
            envProjectid = columns.project_id
            
        projects = Project.objects.filter(id=envProjectid)
        for columns in projects:
            envProject = columns.name
        
        backupenv = Backupenv()
        backupSuccess, backupMessage = backupenv.index(envName, envPath, envDbname, envProject)
        
        response_data = {}
        response_data['success'] = backupSuccess
        response_data['message'] = backupMessage
                    
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
def importenv(request):
    
    if request.is_ajax():
        return HttpResponse(request.POST['envname'])
