from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout

from localenvs.form import LoginForm

class Login(View):
    
    form_class = LoginForm
    template = 'frontend/login.html'
    
    def get(self, request, *args, **kwargs):   
        if request.method == 'GET':
            if request.user.is_authenticated():
                return HttpResponseRedirect('/localenvs/dashboard/')
            else:
                return render_to_response(self.template, context_instance=RequestContext(request))
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login_name']
            password = form.cleaned_data['login_pass']
            user = authenticate(username=username, password=password) 
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/localenvs/dashboard/')
            else:
                return render(request, self.template, {'incorrect_user':'The user do not exist'})
        return render(request, self.template)
    
class Logout(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/localenvs/')