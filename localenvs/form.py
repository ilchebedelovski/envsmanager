from django import forms

class DashboardForm(forms.Form):
    env_name = forms.CharField(label='env_name', max_length=15)
    env_path = forms.CharField(label='env_path', max_length=15)
    env_domain = forms.CharField(label='env_domain', max_length=15)
    env_dbname = forms.CharField(label='env_dbname', max_length=30)
    env_radio = forms.CharField(label='env_radio', max_length=15)
    
class LoginForm(forms.Form):
    login_name = forms.CharField(label='login_name', max_length=15)
    login_pass = forms.CharField(label='login_pass', max_length=15)