import subprocess
import os
import cgi
import cgitb   
from time import gmtime, strftime
import string
import git

class Gitenv(object):
    
    def __init__(self):
        return
    
    def index(self, gitOption, envName, envPath, envProject):
        
        if ( gitOption == 'status' ):
            return self.__gitStatus(envName, envPath)
        elif ( gitOption == 'log' ):
            return self.__gitLog(envName, envPath)
    
    def __gitStatus(self, envName, envPath):
                
        gitCommand = ['/usr/bin/git', 'status', '-s']
        p = subprocess.Popen(gitCommand, cwd=envPath, stdout=subprocess.PIPE)
        p.wait()
        gitLines = p.stdout.readlines()
        
        return gitLines
    
    def __gitLog(self, envName, envPath):
        
        gitCommand = ['/usr/bin/git', 'log']
        p = subprocess.Popen(gitCommand, cwd=envPath, stdout=subprocess.PIPE)
        p.wait()
        gitLines = p.stdout.readlines()
        
        return gitLines
    
    def __gitAdd(self, envName, envPath):
            
        return
    
    def __gitCommit(self, envName, envPath):
        
        return
