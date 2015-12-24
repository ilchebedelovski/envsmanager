import subprocess
import os
import cgi
import cgitb   
from time import gmtime, strftime
import string
    
class Backupenv(object):
    
    DEVUSER = 'developer'
    DEVPASS = 'rYh69WHZ4'
    DEVHOST = 'localhost'
    FILEBACKUPPATH = '/home/html/ecomwiseenvs/_backups/filesystem/'
    DBBACKUPPATH = '/home/html/ecomwiseenvs/_backups/database/'
    BACKUPPATH = '/home/html/ecomwiseenvs/_backups/'
    
    def index(self, envName, envPath, envDbname, envProject):
                
        filesystemOut = os.listdir(self.FILEBACKUPPATH)
        databaseOut = os.listdir(self.DBBACKUPPATH)
        filesystemBackups = []
        databaseBackups = []
        
        for item in filesystemOut:
            separated = string.split(item, '_')
            filesystemBackups.append(separated[1])
            
        for item in databaseOut:
            separated = string.split(item, '_')
            databaseBackups.append(separated[1])
        
        itemCountFilesystem = filesystemBackups.count(envName)
        itemCountDatabase = databaseBackups.count(envName)
        
        if ( itemCountFilesystem > 4 or itemCountDatabase > 4 ):
             return (False, "Too many backups for the same project")
        else:
            filesystemSuccess, filesystemMessage = self.__filesysteBackup(envName, envPath, envProject)
            databaseSuccess, databaseMessage = self.__databaseBackup(envName, envDbname, envProject)
            
            if filesystemSuccess is not True:
                return (filesystemSuccess, filesystemMessage)
            elif databaseSuccess is not True:
                return (databaseSuccess, databaseMessage)
            else:
                return (True, "Filesystem and database backups are located under " + self.BACKUPPATH)
    
    def __filesysteBackup(self, envName, envPath, envProject):
        
        date = strftime("%y%m%d%H%M", gmtime())
        envBackup = self.FILEBACKUPPATH + envProject + '_' + envName + '_' + date + '.tar'
                
        if os.path.isdir(envPath):
            subprocess.call('/bin/tar cf %s %s' %(envBackup, envPath), shell=True)
            return (True, envBackup + " is created")
        else:
            return (False, envPath + " does not exist on the server")
        
    def __databaseBackup(self, envName, envDbname, envProject):
        
        date = strftime("%y%m%d%H%M", gmtime())
        envBackup = self.DBBACKUPPATH + envProject + '_' + envName + '_' + date + '.sql'
                
        try:
            p = subprocess.Popen(['/usr/bin/mysql', '-u', self.DEVUSER, '-p' + self.DEVPASS, '-h', self.DEVHOST, '-Bse', 'show databases'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if err:
                return (False, str(err) + " for " + envDbname)
            else:
                listOfDbs = out.split('\n')
                if envDbname in listOfDbs:
                    subprocess.call('/usr/bin/mysqldump -u %s -p"%s" -h %s %s > %s' %(self.DEVUSER, self.DEVPASS, self.DEVHOST, envDbname, envBackup), shell=True)
                    return (True, 'Database backup is created under ' + envBackup)
                else:
                    return (False, envDbname + ' do not exists')         
        except:
            return (False, "Shell command not executed for creating database dump")
    
        