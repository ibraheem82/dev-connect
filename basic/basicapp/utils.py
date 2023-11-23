from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# ? [results] how many results do we want to allow per page.
def paginateProjects(request, projects, results):
     # ! Getting the first page
    # page = 1
    # ! Getting the seccond page
    # page = 2
    
    # todo-> the page must be an integer, it will be pass in to the paginator button so it will display the number of the page on the browser search url and show the page we are on.
    page = request.GET.get('page')
    
    
    # ! it will give us the query_set and give us the [results] here
    # ! it will give us three results per page.
    paginator = Paginator(projects, results)
    
    try:
        # !Resetting the project variable and index it by a specific page and only get 3 results
        # ! we are going to get 3 projects and we are going to get the first page of those 3 projects
        # ! [ .page ] means what page do we want to get from the query_set
        projects = paginator.page(page)
        # ! [ PageNotAnInteger ] it means that if a page is not passed in, it should be set to 1, we are saying that if the user click on the [projects] link on the navigation bar it should set it to the first page by defuallt.
    except PageNotAnInteger:
        page = 1
        # ! if a user click on the page or just visting the page for the first time it will display the first page which we have set.
        projects = paginator.page(page)
        # ! if the user keep searching the page and there is no more page
        # ! we are saying that if there is no page, so if the user go out of page, it will give the user the last page
    except EmptyPage:
        # ! [  num_pages ] this will tell us how many pages we have
        page = paginator.num_pages
        # ! setting projects to the page value, it is going to give us whatever the last page is.
        projects = paginator.page(page)

    # * Creating how paginator button and pages should be rendered.
    # ! it is representing the left buttons index.
    # ! [page] is the current page we are on
    # ! [ (page - 4) ] means that if we are on page 5 the left index the button will be 1, if you are page 10 the left index will be 5,
    leftIndex = (int(page) - 4)
    # ! if the left index is less 1, so if we are on page 3 and we do (3 - 4) it will gives us a negative value
    
    # TODO : condition to follow
    # ! even though we have 5 pages we should only see 3 at a time.
    # ! if we have a thousands pages, we will never see a thousand pages output like that
    
    if leftIndex < 1:
        leftIndex = 1

    
    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex  = paginator.num_pages + 1
        
        # * Customizing the paginator class
    custom_range = range(leftIndex, rightIndex)
    
    return custom_range, projects










    

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # ! [tags] this is a manytomany field
    
    tags = Tag.objects.filter(name__icontains = search_query)
    
    # ! The [Project] model has a attribute called [tags]
    
        # ! [ distinct() ] will make sure that there is no any duplicate table queryed. i.e it makes sure that anytime we get a queryset we don't get any duplicate so we just return back one table for each instance or one table object

    # * [DISTINCT] eliminates duplicates rows from the query results.
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) | 
        Q(description__icontains = search_query) |
        # ! [tags__in = tags] means if we look for the [tags] queryset in the project does it contains a tag that is in this queryset in this filter
        Q(tags__in = tags) |
        # * Search by project owner
        # ! we are going into the parent object [owner__name] and the attribute name, searching by name
        # ! [owner__name__icontains] it means give us every projects where the owners name [contains] or we can search the name of the person that create a project, it will bring out the project that the person has done.
        Q(owner__name__icontains = search_query)
    )    
    return projects, search_query
