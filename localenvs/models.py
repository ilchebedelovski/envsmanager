from django.db import models

class Project(models.Model):
    
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.id)
        
class Environments(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    dbname = models.CharField(max_length=50)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):                  # __unicode__ method can do whatever it needs to do in order to return a representation of an object
        return u'%s %s %s %s %s' % (self.name, self.path, self.domain, self.dbname, self.project)