# Featured Pages Open ONI Plugin

This plugin allows you to quickly display page images in a "featured content" section.  You can display random pages from all of your titles, or you can configure the plugin to use specifically chosen pages.

## Compatibility

The "main" branch should not be considered stable.  Unlike the core Open ONI
repository, plugins don't warrant the extra overhead of having separate
development branches, release branches, etc.  Instead, it is best to find a tag
that works and stick with that tag.

- Featured Pages v0.4.0 and prior only work with Python 2 and Django 1.11 and prior
  - Therefore these versions of the Featured Pages plugin are only compatible up to
    (and including) ONI v0.11
- Featured Pages releases v0.5.0 and later require Python 3 and Django 2.2, and
  should be used with ONI v0.12 and later

## Setup

The setup for this plugin is slightly involved, but bear with us!

```
git clone git@github.com:open-oni/plugin_featured_content.git onisite/plugins/featured_content
```

Add it to your `INSTALLED_APPS` in `onisite/settings_local.py`, above your theme (`default` or custom themes you've created):

```
INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    'onisite.plugins.featured_content',
    'themes.nebraska',
    'core',
)

```

Put in a new URL path into `onisite/urls.py` above the `core.urls` line.  You can put this plugin at whatever URL you prefer, but two examples are given below.

```
  # this path will overwrite / (home)
  url(r'^$', include("onisite.plugins.featured_content.urls")),

  # this path will put the plugin at /featured_content
  url(r'^featured_content/', include("onisite.plugins.featured_content.urls")),


  # make sure you include your featured_content link above the core urls
  url('', include("core.urls")),
```

Now copy a few configuration / template files
```
cd onisite/plugins/featured_content
cp config_example.py config.py
cp templates/featured_example.html templates/featured.html
```

## Configuration

There are three possible options for the behavior of this plugin:

- random selection from all pages (changes each day)
- "on this day" selection, defaults to random if nothing occurred on that day
- user selected pages of interest

Please find below descriptions of how to configure the plugin for each of the above options.

### Random Selection

`config.py`

```
RANDOM = True
NUMBER = 4      # number of results that will be returned
```

### On This Day

You must first set RANDOM to False to use this feature

`config.py`

```
RANDOM = False
THISDAY = True
MINYEAR = 1750   # earliest year to search for "on this day"
MAXYEAR = 2000   # latest year to search for "on this day"
NUMBER = 4       # number of results that will be returned
```

### User Selection

To get at the user selected featured pages, first set RANDOM and THISDAY to False, then add information for your specifically requested pages.

`config.py`

```
RANDOM = False
THISDAY = False
NUMBER = 4
PAGES = (
  {
      'lccn': 'sn83045350',
      'date': '1878-01-03',
      'edition': 1,
      'sequence': 1,
      'caption': 'Put a caption for your newspaper here'
  },
  {
      'lccn': 'sn83045350',
      'date': '1878-01-03',
      'edition': 1,
      'sequence': 2,
      'caption': 'This is the second page of an issue'
  },
)
```

If you enter more `PAGES` than your max `NUMBER`, a subset will be selected randomly (each day) from your featured set.  You can get the information for lccn, date, edition, and sequence from the URL for an individual page.

`http://newspapers.uni.edu/lccn/sn83045350/1878-01-03/ed-1/seq-1/`

- `edition` will typically always be 1, unless if the paper has morning and evening runs, etc
- `sequence` refers to the page number, so 1 is also a good choice if you want the front page of a particular day


## Customizing the Template

You may want to change the text on the featured content page.  Open up `templates/featured.html` and add any HTML you need in `{% block featured_description %}`


## API use

If you only want to get at the data without using the templates or routing provided, you can do something like this:

```python
# In your theme's views.py:
from onisite.plugins.featured_content import helpers as featured_content_helpers

def home(request):
    """Grab featured content from the plugin, then set up some of the
    high-level data like approximate page count"""
    pages, this_day_title = featured_content_helpers.get_pages()
    approx_pages = "about 900,000 pages"
    earliest_year = 1900
    latest_year = 1900

    return render(request, 'home.html', locals())
```

This function lets you grab the pages and "this_day_title" variable, and then
set up your own variables from other data sources, as well as render whatever
template you want.  The plugin must still be configured, and must still be in
your app list, but you wouldn't add it to your `urls.py`, and you can create a
template however it makes sense with your particular homepage.
