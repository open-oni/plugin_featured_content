import random

from django.shortcuts import render_to_response
from django.template import RequestContext

from onisite.plugins.featured_pages import config
from core import models

def featured(request):
    number = config.NUMBER
    if config.RANDOM:
        page_len = len(models.Page.objects.all())
        select_pages = random.sample(xrange(1, page_len), number)
        pages = map(_get_page_info_by_id, select_pages)
    else:
        # grab randomly from the curated selection
        page_info = config.PAGES
        page_len = len(page_info)
        if page_len <= number:
            pages = map(_get_page_by_info, page_info)
        else:
            rand_nums = random.sample(range(1, page_len), number)
            random_pages = []
            for num in rand_nums:
                random_pages.append(page_info[num])
            pages = map(_get_page_by_info, random_pages)

    return render_to_response('featured.html',
                           dictionary=locals(),
                           context_instance=RequestContext(request))   


# helper methods

def _get_page_info_by_id(page_id):
    page_obj = models.Page.objects.get(id=page_id)
    issue_obj = page_obj.issue
    page = {
        'date': issue_obj.date_issued,
        'edition': issue_obj.edition,
        'lccn': issue_obj.title.lccn,
        'name': issue_obj.title.name,
        'page_obj': page_obj,
        'sequence': page_obj.sequence,
    }
    return page

def _get_page_by_info(page_info):
    try:
        title = models.Title.objects.get(lccn=page_info['lccn'])
        page_info['name'] = title.name
        page_info['page_obj'] = (title
                             .issues.get(edition=page_info['edition'], date_issued=page_info['date'])
                             .pages.get(sequence=page_info['sequence']))
    except:
        page_info['name'] = 'Unknown Title'
        page_info['page_obj'] = None
    return page_info
