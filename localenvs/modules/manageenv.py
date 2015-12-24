import subprocess
import os
import cgi
import cgitb   
    
class Createenv(object):
    
    DEVUSER = 'developer'
    DEVPASS = 'rYh69WHZ4'
    DEVHOST = 'localhost'
    
    def __init__(self):
        return
    
    def index(self, envProject, envName, envPath, envDomain, envDbname):
        
        filesystemSuccess, filesystemMessage = self.__createFilesystem(envPath)
        virtualhostSuccess, virtualhostMessage = self.__createVirtualHost(envProject, envName, envPath, envDomain)
        databaseSuccess, databaseMessage = self.__createDatabase(envDbname)
                
        if filesystemSuccess is not True:
            return (filesystemSuccess, filesystemMessage)
        elif virtualhostSuccess is not True:
            return (virtualhostSuccess, virtualhostMessage)
        elif databaseSuccess is not True:
            return (databaseSuccess, databaseMessage)
        else: 
            return (True, "The environment " + envName + " is created")

    def __createFilesystem(self, envPath):
     
        try:
            os.mkdir(envPath)
            return (True, 'The ' + envPath + 'is created')
        except OSError, e:
            return (False, str(e.args) + " for " + envPath)
         
    def __createVirtualHost(self, envProject, envName, envPath, envDomain):
        
        if os.path.isdir(envPath):
            
            confPath = "/etc/httpd/conf.d/" + envProject + "conf/" + envName + ".conf"
                        
            vHost = ""
            vHost += "<VirtualHost *:80>\n"
            vHost +=    "\tDocumentRoot " + envPath + "\n"
            vHost +=    "\tServerName " + envDomain + "\n"
            vHost +=    "\t<Directory '" + envPath + "'>\n"
            vHost +=        "\t\tAllowOverride All\n"
            vHost +=        "\t\tOptions None\n"
            vHost +=        "\t\tOrder allow,deny\n"
            vHost +=        "\t\tAllow from all\n"
            vHost +=    "\t</Directory>\n"
            vHost += "</VirtualHost>\n"
            vHost += "\n"
            
            if os.path.isfile(confPath):
                try:
                    confFile = open(confPath, "a")
                    confFile.write(vHost)
                    confFile.close()
                    return (True, 'The VirtualHost is appended')
                except IOError, e:
                    return (False, str(e.args) + ' for ' + confPath)
            else:
                try:
                    confFile = open(confPath, "w")
                    confFile.write(vHost)
                    confFile.close()
                    return (True, 'The VirtualHost is created')
                except IOError, e:
                    return (False, str(e.args) + ' for ' + confFile)
        else:
            return (False, "Directory " + envPath + " do not exists")
  
       
    def __createDatabase(self, envDbname):
        
        try:
            p = subprocess.Popen(['/usr/bin/mysql', '-u', self.DEVUSER, '-p' + self.DEVPASS, '-h', self.DEVHOST, '-Bse', 'show databases'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if err:
                return (False, str(err) + " for " + envDbname)
            else:
                listOfDbs = out.split('\n')
                if envDbname in listOfDbs:
                    return (False, "Database " + envDbname + " exists")
                else:
                    subprocess.call('/usr/bin/mysql -u %s -p"%s" -h %s -Bse "CREATE DATABASE %s DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_unicode_ci"' %(self.DEVUSER, self.DEVPASS, self.DEVHOST, envDbname), shell=True)
                    return (True, 'The database ' + envDbname + ' is created')         
        except:
            return (False, "Shell command not executed for removing database")

class Removeenv(object):
    
    DEVUSER = 'developer'
    DEVPASS = 'rYh69WHZ4'
    DEVHOST = 'localhost'
    
    def __init__(self):
        return
    
    def index(self, envProject, envName, envPath, envDomain, envDbname):
        
        filesystemSuccess, filesystemMessage = self.__removeFilesystem(envPath)
        virtualhostSuccess, virtualhostMessage = self.__removeVirtualHost(envProject, envName)
        databaseSuccess, databaseMessage = self.__removeDatabase(envDbname)
        
        if filesystemSuccess is not True:
            return (filesystemSuccess, filesystemMessage)
        elif virtualhostSuccess is not True:
            return (virtualhostSuccess, virtualhostMessage)
        elif databaseSuccess is not True:
            return (databaseSuccess, databaseMessage)
        else:
            return (True, 'The environment ' + envName + ' is removed')
        
    def __removeFilesystem(self, envPath):
        
        if not os.path.exists(envPath):
            return (False, envPath + " do not exist")
        else:        
            try:
                os.rmdir(envPath)
                return (True, "Directory " + envPath + " is removed")
            except OSError, e:
                return (False, str(e.arg) + " On removing environment")
    
    def __removeVirtualHost(self, envProject, envName):
        
        confPath = "/etc/httpd/conf.d/" + envProject + "conf/" + envName + ".conf"     
        if os.path.isfile(confPath):
            try:
                os.remove(confPath)
                return (True, confPath + " is removed")
            except OSError, e:
                return str(e.arg) + " on removing conf file"
        else:
            return (False, confPath + " not found")
    
    def __removeDatabase(self, envDbname):
         
        try:
            p = subprocess.Popen(['/usr/bin/mysql', '-u', self.DEVUSER, '-p' + self.DEVPASS, '-h', self.DEVHOST, '-Bse', 'show databases'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if err:
                return (False, str(err) + " for " + envDbname)
            else:
                listOfDbs = out.split('\n')
                if envDbname in listOfDbs:
                    subprocess.call('/usr/bin/mysql -u %s -p"%s" -h %s -Bse "DROP DATABASE %s"' % (self.DEVUSER, self.DEVPASS, self.DEVHOST, envDbname), shell=True)
                    return (True, envDbname + " is removed")
                else:
                    return (False, "Database " + envDbname + " do not exists")
        except:
            return (False, "Shell command not executed for removing database")

    
    
           