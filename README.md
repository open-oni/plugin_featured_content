# Featured Pages Open ONI Plugin

This plugin allows you to quickly display page images in a "featured content" section.  You can display random pages from all of your titles, or you can configure the plugin to use specifically chosen pages.

## Setup

The setup for this plugin is slightly involved, but bear with us!

```
git clone git@github.com:open-oni/plugin_featured_content.git onisite/plugins/featured_content
```

Add it to your `INSTALLED_APPS` in `onisite/settings_local.py`:

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

Take a look at `config.py`.  There are two settings which are pretty self-explanatory:

```
# Set to True to use random pages instead of curated selections in PAGES
RANDOM = True

# The number of results that will be displayed
NUMBER = 4
```
Setting RANDOM to False will mean that you can use the following setting in the config file:

```
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
      'caption': 'This is the second one'
  },
)
```

Unfortunately, at this time, you need to hand enter the pages that you would like to appear as featured.  If you enter more pages than your max NUMBER, then only that many will be selected at random from your featured set.  You can get the information like lccn, date, edition, and sequence from the URL for an individual page.

`http://newspapers.uni.edu/lccn/sn83045350/1878-01-03/ed-1/seq-1/`

`edition` will typically always be 1, unless if the paper has morning and evening runs, etc
`sequence` refers to the page number, so 1 is also a good choice if you want the front page of a particular day


You may also want to change the text on the featured content page.  Open up `templates/featured.html` and add any HTML you need in `{% block featured_description %}`

You will likely need to restart your app before you see the changes!
