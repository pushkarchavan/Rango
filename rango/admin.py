from django.contrib import admin
from rango.models import Category, Page

# Registering Models

class PageInline(admin.TabularInline):
  model = Page
  extra = 1
  
class CategoryAdmin(admin.ModelAdmin):
  inlines = [PageInline]
  fieldsets = [('Categories', {'fields': ['name']}),]
  list_display = ('name', 'views', 'likes')
  search_fields = ['name']
  

admin.site.register(Category, CategoryAdmin)
