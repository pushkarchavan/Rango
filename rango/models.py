from django.db import models

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=140, unique=True)
  
  def __unicode__(self):
    return self.name
  
class Page(models.Model):
  category = models.ForeignKey(Category)
  title = models.CharField(max_length=140)
  url = models.URLField()
  views = models.IntegerField(default=0)
  likes = models.IntegerField(default=0)
  pub_date = models.DateTimeField('date published')
    
  def __unicode__(self):
    return self.title