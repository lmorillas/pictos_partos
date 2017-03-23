from django.shortcuts import render

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query
from wagtail.wagtailimages.models import Image



def buscapictos(request):
    # Search
    search_query = request.GET.get('query', None)
    
    if search_query:
        search_results = Image.objects.search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Image.objects.none()

    # Render template
    return render(request, 'busqueda_pictos.html', {
        'search_query': search_query,
        'search_results': search_results,
    })