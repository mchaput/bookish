import os
import os.path

from bookish.config import DefaultConfig, expandpath
from bookish.stores import FileStore
from bookish.stores import MountStore
from bookish.stores import ZipTree

from houdinihelp import hcoloring, hpages, hsearch, hstores, htextify
try:
    import hou
except ImportError:
    hou = None


if hou:
    hou_home = hou.homeHoudiniDirectory()
elif "HOUDINI_USER_PREF_DIR" in os.environ:
    hou_home = os.environ["HOUDINI_USER_PREF_DIR"]
else:
    hou_home = "."

if "HOUDINI_VERSION" in os.environ:
    version = os.environ["HOUDINI_VERSION"]
    major_version, minor_version, build_version = version.split(".")
else:
    version = major_version = minor_version = build_version = ""


def houdini_docs(doc_dir, add_houdini_path=False, with_zip=False):
    # Returns a list of Store objects

    # Copy the default bookish list of stores which includes the base templates,
    # grammar files, and static files
    docs = list(DefaultConfig.DOCUMENTS)
    # Add the documentation directory
    docs.append(FileStore(doc_dir))

    # Look for special directories relative to this Python module
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Add Houdini-specific templates
    templates_store = FileStore(os.path.join(base_dir, "templates"))
    docs.append(MountStore(templates_store, "/templates"))

    # Add Houdini-specific static files
    static_store = FileStore(os.path.join(base_dir, "static"))
    docs.append(MountStore(static_store, "/static"))

    if hou:
        # Add HOM sources (nodes, shelf tools) to virtual file system
        docs.append(hstores.HoudiniStore())

        if add_houdini_path:
            # Get all HOUDINIPATH/help directories
            try:
                helpdirs = hou.findDirectories("help")
            except hou.OperationFailed:
                helpdirs = []
            # Add FireStores for them
            docs += [FileStore(hd) for hd in helpdirs]

    if with_zip:
        # Add a storage overlay to read files out of any zip files in the root
        # directory
        docs.append(ZipTree(doc_dir))

    return docs


class HoudiniBaseConfig(DefaultConfig):
    # Use a custom WikiPages class to get Houdini-specific page processors
    PAGES_CLASS = hpages.HoudiniPages
    # Use a custom Searchables class to get Houdini-specific indexed fields
    SEARCHABLES = hsearch.HoudiniSearchables()

    # Virtual path to the template to use for wiki pages
    DEFAULT_TEMPLATE = "/templates/hpage.jinja2"
    # Virtual path to the template to use for search results
    SEARCH_TEMPLATE = "/templates/hsearch.jinja2"

    # Houdini-specific search shortcuts
    SHORTCUTS = [
        {"shortcut": "n", "query": "type:node", "desc": "All nodes"},
        {"shortcut": "s", "query": "category:node/sop",
         "desc": "Geometry nodes (SOPs)"},
        {"shortcut": "d", "query": "category:node/dop",
         "desc": "Dynamics nodes (DOPs)"},
        {"shortcut": "o", "query": "category:node/obj",
         "desc": "Object nodes"},
        {"shortcut": "v",
         "query": "(category:vex OR category:node/vop)",
         "desc": "VEX and VOPs"},
        {"shortcut": "r", "query": "(category:node/out OR type:property)",
         "desc": "Rendering"},
        {"shortcut": "p", "query": "category:hom*",
         "desc": "Python scripting (HOM)"},
        {"shortcut": "e", "query": "type:expression",
         "desc": "Expression functions"},
    ]

    EXTRA_SHORTCUTS = []

    # Houdini specific category ordering in search results
    CATEGORIES = """
    _ tool node/sop node/dop node/obj node/vop node/out node/cop2 node/chop
    vex example homclass hommethod homfunction hommodule
    expression hscript property
    """

    # Houdini specific Pygments lexers
    VEX_LEXER = hcoloring.VexLexer
    HSCRIPT_LEXER = hcoloring.HScriptLexer
    TEXTIFY_CLASS = htextify.HoudiniTextifier

    AUTO_COMPILE_SCSS = False

    VARS = DefaultConfig.VARS
    VARS["HOUDINI_VERSION"] = version
    VARS["MAJOR_VERSION"] = major_version
    VARS["MINOR_VERSION"] = minor_version
    VARS["BUILD_VERSION"] = build_version


class HoudiniDevConfig(HoudiniBaseConfig):
    if "SH" in os.environ:
        houdini_base = expandpath("$SH/")
    else:
        houdini_base = expandpath("~/dev/src/houdini")

    DEBUG = True
    DOCUMENTS = houdini_docs(os.path.join(houdini_base, "help/documents"),
                             add_houdini_path=False)

    EDITABLE = True

    # Add the icons source directory
    icons_store = FileStore(os.path.join(houdini_base, "support/icons"))
    DOCUMENTS.append(MountStore(icons_store, "/icons"))

    # Store the cache and search index in the docs build directory
    build_dir = os.path.join(houdini_base, "help/build")
    CACHE_DIR = os.path.join(build_dir, "cache")
    INDEX_DIR = os.path.join(build_dir, "index")

    ENABLE_BACKGROUND_INDEXING = False
    AUTO_COMPILE_SCSS = True


class HoudiniAppConfig(HoudiniBaseConfig):
    doc_dir = expandpath("$HFS/houdini/help")
    build_dir = expandpath(hou_home + "/config/Help")

    DEBUG = False

    # Copy the default bookish file system which includes the base templates,
    # grammar files, and static files
    DOCUMENTS = houdini_docs(doc_dir, add_houdini_path=True, with_zip=True)

    # Store the cache in the user's prefs dir
    CACHE_DIR = os.path.join(build_dir, "cache")

    INDEX_DIR = expandpath("$HFS/houdini/config/Help/index")
    ENABLE_BACKGROUND_INDEXING = False
    AUTO_COMPILE_SCSS = False

    # Get the read-only index of the "factory" files from $HFS
    # STATIC_INDEX_DIR = expandpath("$HFS/houdini/config/Help/index")
    # Store the dynamic index in the user's prefs dir
    # INDEX_DIR = os.path.join(build_dir, "index")

    LOGLEVEL = "WARNING"
    # LOGFILE = os.path.join(build_dir, "bookish.log")
