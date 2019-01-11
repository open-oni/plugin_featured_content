import random
import datetime
from core import models
from onisite.plugins.featured_content import config

def get_pages():
    """Seed the RNG to get random featured pages.  This function can be used
    from other plugins or themes without using this plugin's templates or urls
    if desired."""
    # Seed the RNG with today's date so we always feature the same page(s) for
    # an entire day
    random.seed(datetime.date.today().strftime("%Y%m%d"))

    # Get pages and randomize where necessary
    pages, this_day_title = _get_pages()

    # Clear the seed so anything else using random numbers isn't affected
    random.seed(None)

    return pages, this_day_title

# "private" helper methods

def _get_pages():
    """Delegate page-fetching based on the configuration; if THISDAY is
    requested and gets valid pages, the second argument returned is True to
    signal to the template which title to use"""

    # We use random pages if explicitly requested *or* THISDAY is requested but
    # no pages are found
    isrand = config.RANDOM or config.THISDAY

    if config.THISDAY:
        pages = _pages_this_day()
        if len(pages) > 0:
            return pages, True

    if isrand:
        return _random_pages(config.NUMBER), False

    return _featured_pages(config.PAGES, config.NUMBER), False

def _featured_pages(pages, limit):
    feat_pages = map(_get_page_by_info, pages)
    # remove requested pages which were not found in the database
    feat_pages = filter(None, feat_pages)
    if len(feat_pages) <= limit:
        return feat_pages
    else:
        pages = []
        rand_nums = random.sample(xrange(len(feat_pages)), limit)
        for num in rand_nums:
            pages.append(all_pages[num])
        return pages

def _pages_this_day():
    """Find any pages within the min/max years and today's month/year"""
    pages = []

    # Filtering variables
    dt_range_start = datetime.date(config.MINYEAR, 1, 1)
    dt_range_end = datetime.date(config.MAXYEAR, 12, 31)
    now = datetime.date.today()

    # Grab each issue that matches, and create a page_info structure for the
    # first page of that issue.  Grabbing only the set number requested by user
    issues = models.Issue.objects
    issues = issues.filter(date_issued__range=(dt_range_start, dt_range_end))
    issues = issues.filter(date_issued__month = now.month)
    issues = issues.filter(date_issued__day = now.day)
    for issue in issues[:config.NUMBER]:
        first_page = issue.first_page
        if first_page and first_page.jp2_filename:
            pages.append({
                'date': issue.date_issued,
                'edition': issue.edition,
                'lccn': issue.title.lccn,
                'name': issue.title.name,
                'page_obj': first_page,
                'sequence': first_page.sequence,
            })

    return pages

def _random_pages(limit):
    page_len = models.Page.objects.count()
    if page_len:
        indices = []
        pages = []
        if page_len < limit:
            indices = [i for i in xrange(page_len)]
        else:
            indices = random.sample(xrange(page_len), limit)

        page_objects = models.Page.objects.all()
        for index in indices:
            pages.append(page_objects[index])

        return map(_get_page_by_object, pages)
    else:
        return []

def _get_page_by_object(page_obj):
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
        # if there is no record in the database for a particular page, then set to None
        if page_info['page_obj'] is None:
            page_info = None
    except:
        page_info = None
    return page_info
