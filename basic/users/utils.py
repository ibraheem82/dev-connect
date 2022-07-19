# from jmespath import search
from .models import Profile, Skill
from django.db.models import Q

# * You should import this in your views file.

# ! Be in charge of executing [search] functionality.
def searchProfiles(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        # ! find the [skill] and see if it is inside the query
        # ! search the [skills] is that query [name__iexact = search_query] matches perfectly
    skills = Skill.objects.filter(name__icontains = search_query)
    # print('SEARCH:', search_query)
    # ! [ distinct() ] will make sure that there is no any duplicate table queryed. i.e it makes sure that anytime we get a queryset we don't get any duplicate so we just return back one table for each instance or one table object

    # * [DISTINCT] eliminates duplicates rows from the query results.
    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) |
                                                 Q(short_intro__icontains = search_query) |
                                                 # ? Does the [profiles] have the skill that is listed in the queryset [skills]
                                                 Q(skill__in = skills)
                                                )
    
    return profiles, search_query