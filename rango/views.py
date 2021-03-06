from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page

# Create your views here.
def index(request):
  # Obtain the context from HTTP request
  context = RequestContext(request)
  
  # Query the database for a list of ALL categories currently stored.
  # Order the categories by no. likes in descending order.
  # Retrieve the top 5 only - or all if less than 5.
  # Place the list in our context_dict dictionary which will be passed to the template engine.
  category_list = Category.objects.order_by('-likes')[:5]
  context_dict = {'categories': category_list}
  page_list = Page.objects.order_by('-likes')[:5]
  context_dict['pages'] = page_list
  
  # The following two lines are new.
  # We loop through each category returned, and create a URL attribute.
  # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
  for category in category_list:
    category.url = category.name.replace(' ', '_')
  #for page in page_list:
  #  page.link = page.title.replace(' ', '_')
  
  # Return a rendered response to send to the client.
  # We make use of the shortcut function to make our lives easier.
  # Note that the first parameter is the template we wish to use.
  return render_to_response('rango/index.html', context_dict, context)
  
def about(request):
  context = RequestContext(request)
  context_dict = {'rango_user' : 'Admin' , 'boldmessage' : 'You are awesome'}
  return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):
  # Request our context
  context = RequestContext(request)
  
  # Change underscores in the category name to spaces.
  # URLs don't handle spaces well, so we encode them as underscores.
  # We can then simply replace the underscores with spaces again to get the name.
  category_name = category_name_url.replace('_', ' ')
  
  # Create a context dictionary which we can pass to the template rendering engine.
  # We start by containing the name of the category passed by the user.
  context_dict = {'category_name': category_name}
  
  try:
    # Can we find a category with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # So the .get() method returns one model instance or raises an exception.
    category = Category.objects.get(name=category_name)
    
    # Retrieve all of the associated pages.
    # Note that filter returns >= 1 model instance.
    pages = Page.objects.filter(category=category)
    
    # Adds our results list to the template context under name pages.
    context_dict['pages'] = pages
    # We also add the category object from the database to the context dictionary.
    # We'll use this in the template to verify that the category exists.
    context_dict['category'] = category
    
  except Category.DoesNotExist:
    # We get here if we didn't find the specified category.
    # Don't do anything - the template displays the "no category" message for us.
    pass
  
  # Go render the response and return it to the client.
  return render_to_response('rango/category.html', context_dict, context)

# TODO Understand this view
def add_category(request):
  context = RequestContext(request)
  
  # A HTTP POST?
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    
    # Have we been provided with a valid form?
    if form.is_valid():
      # Save the new category to the database.
      form.save(commit=True)
      
      # Now call the index() view.
      # The user will be shown the homepage.
      return index(request)
    else:
      # The supplied form contained errors - just print them to the terminal.
      print form.errors
  else:
    # If the request was not a POST, display the form to enter details.
    form = CategoryForm()
    
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
  return render_to_response('rango/add_category.html', {'form': form}, context)
  