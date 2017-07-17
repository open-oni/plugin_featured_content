import random
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from onisite.plugins.featured_content import config
from core import models

def featured(request):
    number = config.NUMBER
    pages = None
    if config.THISDAY:
        pages = _this_day()
        if not pages is None:
            this_day_title = True
    if pages is None and config.RANDOM:
        page_len = len(models.Page.objects.all())
        select_pages = random.sample(xrange(1, page_len), number)
        pages = map(_get_page_info_by_id, select_pages)
    elif pages is None:
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

def _this_day():
    pages = []
    today = datetime.date.today()
    rand_years = random.sample(xrange(config.MINYEAR,config.MAXYEAR), config.MAXYEAR-config.MINYEAR)
    rand_years.insert(0, today.year-100)
    for rand_year in rand_years:
        page = _get_page_by_date(today.replace(year = rand_year))
        if not page is None:
            pages.append(page)
            return pages
    return None

def _get_page_by_date(date):
    issues = list(models.Issue.objects.filter(date_issued=date)[:10])
    issue_count = len(issues)
    if issue_count < 1:
        return None
    if issue_count < 2:
        rand_indices = [0]
    else:
        rand_indices = random.sample(xrange(issue_count), issue_count)
    for rand_index in rand_indices:
        issue = issues[rand_index]
        first_page = issue.first_page
        if first_page and first_page.jp2_filename:
            page = {
                'date': issue.date_issued,
                'edition': issue.edition,
                'lccn': issue.title.lccn,
                'name': issue.title.name,
                'page_obj': first_page,
                'sequence': first_page.sequence,
            }
            return page
    return None
