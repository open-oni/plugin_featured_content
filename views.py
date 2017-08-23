import random
import datetime

from django.shortcuts import render

from onisite.plugins.featured_content import helpers

def featured(request):
    all_pages, this_day_title = helpers.get_pages()
    return render(request, 'featured.html', locals())
