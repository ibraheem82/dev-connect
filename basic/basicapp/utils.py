from .models import Project, Tag
from django.db.models import Q

def searchProjects(request):
    
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # ! [tags] this is a manytomany field
    
    tags = Tag.objects.filter(name__icontains = search_query)
    
    # ! A [Project] model has a attribute called [tags]
    
        # ! [ distinct() ] will make sure that there is no any duplicate table queryed. i.e it makes sure that anytime we get a queryset we don't get any duplicate so we just return back one table for each instance or one table object

    # * [DISTINCT] eliminates duplicates rows from the query results.
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) | 
        Q(description__icontains = search_query) |
        # ! [tags__in = tags] means if we look for the [tags] queryset in the project does it contains a tag that is in this queryset in this filter
        Q(tags__in = tags) |
        # * Search by project owner
        # ! we are going into the parent object [owner__name] and the attribute name, searching by name
        # ! [owner__name__icontains] means give us every projects where the owners name [contains]
        Q(owner__name__icontains = search_query)
    )
    # ! ['search_query' : search_query] means that we want what we have searched to be in the input form
    
    return projects, search_query
