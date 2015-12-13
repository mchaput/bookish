import os.path

from bookish import search, stores, textify, wikipages
from bookish.stores import MountStore as Ms
from bookish.stores import FileStore as Fs


def expandpath(path):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


class DefaultConfig(object):
    # Flask configuration

    SECRET_KEY = 'dummy'
    DEBUG = False

    # Directories

    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Bookish configuration

    # Some variables that can be used in templates
    VARS = {}
    ICON_32 = "/images/logos/logo_32.png"
    ICON_144 = "/images/logos/logo_144.png"
    PYGMENTS_CSS = "/static/css/pygments/brightcolor.css"

    # A Storage object containing the documents available to the wiki view
    DOCUMENTS = [
        Ms(Fs(base_dir + "/templates"), "/templates"),
        Ms(Fs(base_dir + "/grammars"), "/grammars"),
        Ms(Fs(base_dir + "/static"), "/static"),
    ]

    # Directory of SCSS files to compile into CSS
    SCSS_ASSET_DIR = "/static/scss/"

    # True if documents should be editable in the browser
    EDITABLE = False

    # Virtual path to the template to use for wiki pages
    DEFAULT_TEMPLATE = "/templates/page.jinja2"
    # Virtual path to the template to use for search results
    SEARCH_TEMPLATE = "/templates/search.jinja2"

    # A bookish.wikipages.WikiPages subclass to use to generate wiki pages
    PAGES_CLASS = wikipages.WikiPages
    # A system file path to a directory in which to store cache files
    CACHE_DIR = "./cache"

    # A system file path to a directory in which to store the full-text index
    INDEX_DIR = "./index"
    # A bookish.search.Searchables instance to use to translate wiki pages into
    # searchable information
    SEARCHABLES = search.Searchables()
    # True if the server should run an indexing thread in the background
    ENABLE_BACKGROUND_INDEXING = False
    # Number of seconds between background indexing runs
    BACKGROUND_INDEXING_INTERVAL = 60

    # Stash an automatic checkpoint while editing
    AUTOSAVE = True
    # Max number of seconds between stashing automatic checkpoint
    AUTOSAVE_SECONDS = 10
    # Max number of checkpoints to save
    CHECKPOINT_MAX = 10

    # A bookish.coloring.SyntaxColorer instance to use for coloring code blocks
    COLORERS = ""

    # A bookish.textify.Textifier subclass to use for translating wiki pages
    # into plain text
    TEXTIFY_CLASS = textify.TextifierBase

    # The base name for directory index pages
    INDEX_PAGE_NAME = "_index"
    # The file extension for wiki pages
    WIKI_EXT = ".txt"
    # The default language for wiki pages
    DEFAULT_LANGUAGE = "en-us"
    # The default locale for wiki pages
    DEFAULT_LOCALE = "en_US"

    # A space-separated string setting the order of categories in search results
    CATEGORIES = ""

    # A list of {"shortcut": "x", "query": "type:x", "desc": "Description"}
    # dictionaries, specifying search shortcuts
    SEARCH_SHORTCUTS = []


class TestConfig(DefaultConfig):
    DEBUG = True
