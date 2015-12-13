import functools
import imp
import os.path
import re
import sys
from collections import namedtuple

from bookish import paths, textify, util, functions, stores
from bookish.compat import u, urlparse


bookish_app = None
bookish_searcher = None

table_to_dir = {
    "Object": "obj",
    "Sop": "sop",
    "Tsop": "tsop",
    "Particle": "part",
    "Pop": "pop",
    "Dop": "dop",
    "ChopNet": "chopnet",
    "Chop": "chop",
    "Driver": "out",
    "Shop": "shop",
    "Cop2": "cop2",
    "CopNet": "copnet",
    "Vop": "vop",
    "VopNet": "vex",
}

dir_to_table = dict([(v, k) for k, v in table_to_dir.items()])

load_script_path = ("$HFS/houdini/python%s.%slibs/loadHelpcardOTLExample.py"
                    % sys.version_info[:2])

tooltip_regex = re.compile('"""(.*?)"""', re.DOTALL)


# Simple memoization decorator to speed up lookups
def memoize(func):
    memo = {}

    @functools.wraps(func)
    def caching_func(*args):
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]
    return caching_func


# getHelpForId
# getParmTooltip
# getParsedHtmlHelp
# getParsedTooltip
# getTooltip
# hasHelp
# load_example
# open_wiki_preview
# startHelpServer
# urlToPath


# API functions

def initialize(*args, **kwargs):
    from houdinihelp.server import get_houdini_app

    global bookish_app
    bookish_app = get_houdini_app(dev=False)


def getHelpForId(helpid):
    s = get_searcher()
    doc = s.document(helpid=helpid)
    if doc:
        return str(doc["path"])


def getParmTooltip(op_table_name, op_type, version, namespace, scopeop,
                   parm_token, parm_label, is_spare):
    pages = get_pages()

    # Load the page
    path = components_to_path(op_table_name, scopeop, namespace, op_type,
                              version)
    try:
        jsondata = pages.json(path, postprocess=False)
    except stores.ResourceNotFoundError:
        # No docs for this node at all
        return None

    if jsondata:
        # Try to find the given parameter
        parmblock = find_parm(jsondata, parm_token, parm_label)
        if parmblock:
            text = functions.first_subblock_string(parmblock)
            return hstring(text)

    # If we didn't find the parameter, and it's a spare parameter, assume it's
    # a render property and try to look it up in the properties
    if is_spare:
        s = get_searcher()
        fields = s.document(path=u"/props/mantra#%s" % parm_token)
        if fields and "summary" in fields:
            return hstring(fields["summary"])


def urlToPath(url):
    """
    Translates a URL from Houdini (e.g. "op:Sop/copy") and translates it into
    a help server path (e.g. "/nodes/sop/copy").
    """

    parsed = urlparse.urlparse(url)

    # urlparse.parse_qs properly returns a dictionary mapping to LISTS of
    # values, since a query string can have repeated keys, but we don't need
    # that capability so we'll just turn it into a dict mapping to the first
    # value
    qs = dict((key, vallist[0]) for key, vallist
              in urlparse.parse_qs(parsed.query).items())

    if parsed.scheme in ("op", "operator"):
        table, name = parsed.path.split("/")
        if table.endswith("_state"):
            return "/shelf/" + name

        version = qs.get("version")
        path = components_to_path(table, qs.get("scopeop"), qs.get("namespace"),
                                  name, version)

        pages = get_pages()
        if not pages.exists(path) and version is not None:
            path = components_to_path(table, qs.get("scopeop"),
                                      qs.get("namespace"), name, None)
        return path

    elif parsed.scheme == "parm":
        s = get_searcher()
        r = s.reader()
        table, name, parmname, parmlabel = parsed.path.split("/")
        nodepath = components_to_path(table, qs.get("scopeop"),
                                      qs.get("namespace"), name,
                                      qs.get("version"))
        path1 = "%s#%s" % (nodepath, parmname)
        path2 = "%s#%s" % (nodepath, util.make_id(parmlabel))
        if ("path", path1) in r:
            return path1
        else:
            return path2

    elif parsed.scheme == "gallery":
        table, name, entry = parsed.path.split("/")
        nodepath = components_to_path(table, qs.get("scopeop"),
                                      qs.get("namespace"), name,
                                      qs.get("version"))
        return "/gallery/" + nodepath

    elif parsed.scheme == "tool":
        return "/shelf/" + parsed.path

    elif parsed.scheme == "prop":
        # Replace any versioned mantraX.X with just "mantra"
        path = re.sub("^mantra[0-9.]+", "mantra", parsed.path)
        page, name = path.split("/")
        return "/props/%s#%s" % (page, name)

    elif parsed.scheme == "expr":
        return "/expressions/" + parsed.path

    elif parsed.scheme == "hscript":
        return "/commands/" + parsed.path

    elif parsed.scheme == "opdef":
        return "/nodes/" + parsed.path

    elif parsed.scheme == "vex":
        return "/vex/functions/" + parsed.path

    elif parsed.scheme == "pypanel":
        return "/pypanel/" + parsed.path


def hasHelp(url):
    """
    Returns True if the URL is something the help system can handle, e.g.
    "op:Object/geo".

    This function should go away, and Houdini should just assume the help system
    will deal with schemes other than http/https.
    """

    pages = get_pages()
    path = urlToPath(url)
    if path:
        return pages.exists(path)
    else:
        return False


def getTooltip(url):
    path = urlToPath(url)
    if not path:
        return None

    s = get_searcher()
    doc = s.document(path=u(path))
    if doc:
        summary = doc.get("summary")
        if summary:
            return textify.dechar(summary).encode("utf8")


def getFormattedTooltip(url):
    path = urlToPath(url)
    if not path:
        return

    pages = get_pages()
    s = get_searcher()
    html = pages.html(path, templatename="/templates/plain.jinja2",
                      stylesname="/templates/tooltip.jinja2", searcher=s)
    return html


def getParsedHtmlHelp(url, content):
    if content.lstrip().startswith("<"):
        return content

    path = urlToPath(url)
    if not path:
        return

    pages = get_pages()
    return pages.preview(path, content)


def getParsedTooltip(url, content):
    if content.lstrip().startswith("<"):
        # TODO: Pull a tooltip out of raw HTML
        return None

    path = urlToPath(url)
    if not path:
        return

    pages = get_pages()
    json = pages.string_to_json(path, content, postprocess=False)
    body = json.get("body", ())
    summary = functions.first_subblock_of_type(body, "summary")
    if summary:
        return functions.string(summary)


def startHelpServer(port=48626):
    import socket, threading
    from werkzeug import serving

    max_attempts = 20
    http = None

    server = None
    server_port = port
    for i in range(max_attempts):
        try:
            # TODO: Use host specified by .ini configuration.
            server = serving.make_server("0.0.0.0", server_port, app=bookish_app)
            break
        except socket.error:
            server_port += 1
            pass

    if not server:
        raise Exception("Could not find open port for help server.")

    serverthread = threading.Thread(target=server.serve_forever)
    serverthread.start()

    return server_port


def nodeHelpTemplate(table, namespace, name, version):
    env = bookish_app.jinja_env
    template = env.get_template('/templates/wiki/node_help.jinja2')
    return template.render(table=table, namespace=namespace, name=name,
                           version=version)


# Functions for indexing example usages

def gather_node_paths(node, pathset):
    nodetype = node.type()
    tablename = nodetype.category().name()
    typename = nodetype.name()

    if not(typename.endswith("net") or tablename in ("VopNet", "Manager")):
        path = nodetype_to_path(nodetype)
        pathset.add(path)

    for n in node.children():
        gather_node_paths(n, pathset)


# This function should not really be in the houdinihelp API
def open_wiki_preview(baseurl, path, content):
    import webbrowser
    import tempfile

    pages = get_pages()
    searcher = get_searcher()
    assert path.startswith("/")

    # baseurl is the base URL of the server this page would be coming from if it
    # were real (e.g. the help server). path is the absolute server path; join
    # it to the server's base URL to get the page's URL
    pageurl = baseurl + path[1:]

    # Parse the wiki content into HTML
    html = pages.preview(path, content, searcher=searcher,
                         extras={"baseurl": pageurl})

    # Write the parsed HTML to a temporary file
    fileno, name = tempfile.mkstemp(prefix="preview_", suffix=".html")
    with os.fdopen(fileno, "wb") as f:
        f.write(html)

    # Open the temp file in the default web browser
    webbrowser.open(name)


# Helper functions

def get_pages():
    from bookish import flaskapp

    return flaskapp.get_wikipages(bookish_app)


def get_searcher():
    global bookish_searcher

    if bookish_searcher is None or not bookish_searcher.up_to_date():
        from bookish import flaskapp

        indexer = flaskapp.get_indexer(bookish_app)
        bookish_searcher = indexer.searcher()

    return bookish_searcher


def hstring(text):
    return textify.dechar(functions.string(text)).encode("utf8")


def find_parm(root, parmid, label):
    """
    Tries to find a parameter in a help document, based on the parameter ID and
    its label.
    """

    from bookish.util import dump_tree

    section = functions.subblock_by_id(root, "parameters")
    if section:
        parameters = functions.find_items(section, "parameters_item")
        for parmblock in parameters:
            if functions.block_id(parmblock) == parmid:
                return parmblock
            elif functions.string(parmblock.get("text")).strip() == label:
                return parmblock


def load_example(source, launch=False):
    global index, manager
    global _PYTHON_PANEL_EXAMPLE

    # Convert string to boolean
    # launch = str(launch).lower() == "true"

    if bookish_app is None:
        # If the flask app is None, then houdinihelp.initialize() was not
        # called.
        #
        # If initialize() was not called, then this function must be running
        # inside a central help server.  In which case, we will not be able to
        # load examples in this process.  So we raise an exception and exit
        # early.
        raise Exception("Cannot load example from a central help server.")

    import hou

    ext = paths.extension(source)
    if ext not in (".hda", ".otl", ".pypanel"):
        hou.ui.displayMessage("Don't know how to load example file %r"
                              % source, severity=hou.severityType.Error)
        return

    if launch:
        # Launch a new Houdini to load the example
        # We'll use the HScript 'unix' command instead of shelling out
        # from Python just so we know $HFS will work...
        command = "unix %s %s %s" % (hou.applicationName(), load_script_path,
                                     source)
        hou.hscript(command)
    elif source.endswith(".pypanel"):
        # We need to open a Python Panel in the desktop which can only be done
        # by the main thread.  So we register a callback with Houdini's event
        # loop to guarantee that the actual work is executed in the main thread.
        _PYTHON_PANEL_EXAMPLE = source
        hou.ui.addEventLoopCallback(_load_python_panel_example)
    else:
        # Load the OTL into Houdini and instantiate the first Object asset we
        # find inside
        hou.hda.installFile(source)
        target_hda = None
        hda_defs = hou.hda.definitionsInFile(source)
        for hda in hda_defs:
            if hda.nodeTypeCategory().name() == "Object":
                target_hda = hda
                break

        if target_hda is None:
            hou.ui.displayMessage("Could not find example HDA in OTL file %r"
                                  % source, severity=hou.severityType.Error)

        nodetypename = hda.nodeType().name()
        objnet = hou.node("/obj")
        hda_node = objnet.createNode(nodetypename, exact_type_name=True)

        # Make sure that the HDA node is unlocked so that the user can play
        # around with it.
        propagate = True
        hda_node.allowEditingOfContents(propagate)


_PYTHON_PANEL_EXAMPLE = None
def _load_python_panel_example():
    global _PYTHON_PANEL_EXAMPLE

    # Immediately remove ourselves from the event loop.
    # We should do this first in case a problem occurs further below.
    # We don't want the event loop to keep calling this function if there is an error.
    import hou
    hou.ui.removeEventLoopCallback(_load_python_panel_example)

    if _PYTHON_PANEL_EXAMPLE is None:
        return

    # Install .pypanel file and load interfaces defined in file.
    hou.pypanel.installFile(_PYTHON_PANEL_EXAMPLE)
    pypanel_defs = hou.pypanel.interfacesInFile(_PYTHON_PANEL_EXAMPLE)
  
    # Add loaded interface to the menu.  Check to see if there is a
    # reference already in the menu to avoid duplicate entries.
    menu = hou.pypanel.menuInterfaces()
    for panel in pypanel_defs:
        menu_contains = False
        for menu_item in menu:
            if menu_item == panel.name():
                menu_contains = True
        if not menu_contains:
            menu = menu + (panel.name(),)
    hou.pypanel.setMenuInterfaces(menu) 

    # Locate a Python Panel to load the example interface into.
    desktop = hou.ui.curDesktop()
    python_panel = desktop.paneTabOfType(hou.paneTabType.PythonPanel)
    if python_panel is None:
        python_panel = desktop.createFloatingPaneTab(hou.paneTabType.PythonPanel)

    # Load the interface into the panel.
    python_panel.setActiveInterface(pypanel_defs[0])

    _PYTHON_PANEL_EXAMPLE = None


def components_to_path(table, scopeop, ns, name, version):
    parts = ["/nodes/"]
    if scopeop:
        parts.extend(["--", scopeop.replace("::", "--"), "/"])
    if ns:
        parts.extend(["-", ns, "/"])

    parts.extend([table_to_dir[table], "/"])
    parts.append(name)

    if version is not None:
        parts.extend(["-", version])

    return "".join(parts)


def nodetype_to_path(nodetype):
    """
    Takes a ``hou.NodeType`` object and returns the equivalent help path.
    """

    import hou
    cffntn = hou.hda.componentsFromFullNodeTypeName

    table = nodetype.category().name()
    fullname = nodetype.name()
    scopeop, namespace, corename, version = cffntn(fullname)
    return components_to_path(table, scopeop, namespace, corename, version)


# A regular expression to extract components from a node path
help_exp = re.compile("""
# This regex parses node info out of a virtual path request
/nodes/  # assets are always in this tree
(--(?P<scope>[^/]*)/)?  # Optional scope op dir, with :: replaced by --
(-(?P<ns>[^/]*)/)?  # Optional namespace dir, starts with -
(?P<dir>[^/]+)/  # Node category dir name (e.g. sop, dop)
(?P<name>[^/;]+)  # Node name (e.g. clean), possibly including version
([/;](?P<section>.*))?  # Optional reference to a section inside the asset
""", re.VERBOSE)


NodeInfo = namedtuple('NodeInfo',
                      ['table', 'scopeop', 'namespace', 'corename', 'version',
                       'ext', 'section'],
                      verbose=False)


def path_to_components(path):
    """
    Takes a help path and returns a named tuple of the following components:

    * ``table`` - the node category name, e.g. ``Object``.
    * ``scopeop`` - if the node has a scope, the name of the scope node,
        otherwise an empty string.
    * ``namespace`` - the node's namespace, or an empty string.
    * ``name`` - the node's "core" name.
    * ``version`` - the node's version string.
    * ``ext`` - the filename extension given in the path (if any).
    * ``section`` - an asset section name, or an empty string.
    """

    match = help_exp.match(path)
    if not match:
        return None

    dirname = match.group("dir")
    if dirname not in dir_to_table:
        return None
    table = dir_to_table[dirname]

    namespace = match.group("ns")
    scopeop = match.group("scope")
    if scopeop:
        scopeop = scopeop.replace("--", "::")

    name = match.group("name")
    # Separate the extension
    corename, ext = paths.split_extension(name)

    version = None
    if "-" in corename:
        corename, version = corename.rsplit("-", 1)

    section = match.group("section")
    if section and section.startswith("/"):
        section = section[1:]

    return NodeInfo(table, scopeop, namespace, corename, version, ext, section)


def path_to_nodetype(path):
    try:
        import hou
    except ImportError:
        return None

    info = path_to_components(path)
    if info is None:
        return None

    # In the NodeInfo tuple, version=None means there was no version specified
    # in the path, whereas version='' means the version is the empty string
    version = info.version

    type_cat = hou.nodeTypeCategories()[info.table]
    typedict = type_cat.nodeTypes()

    # Get a node type
    fullname = hou.hda.fullNodeTypeNameFromComponents(
        info.scopeop, info.namespace, info.corename, version or ''
    )
    nodetype = typedict.get(str(fullname))

    # If a path doesn't explicitly specify a version, it means "use the latest
    # version". Unfortunately finding the latest version is not easy in HOM.
    if nodetype and version is None:
        # namespaceOrder() returns a list of node type full names that have the
        # same core name, but potentially different namespaces. So we have to
        # look at each one to find the first that matches our criteria
        for fullname in nodetype.namespaceOrder():
            # Break the fullname into components
            (
                this_scope, this_ns, this_corename, this_version
            ) = hou.hda.componentsFromFullNodeTypeName(fullname)
            if this_scope == info.scopeop and this_ns == info.namespace:
                nodetype = typedict.get(fullname)

    return nodetype


def load_module_from_houdini(
        module_name, search_distro=True, search_houdini_modules=True):
    # Windows always uses modules inside $HFS.
    if sys.platform.startswith("win"):
        return

    # Find the location(s) of modules inside $HFS.
    module_search_path = []
    if search_distro:
        if sys.platform == "darwin":
            python_framework_dir = (
                "$HFS/Frameworks/Python.framework/Versions/%i.%i" % (
                    sys.version_info[0], sys.version_info[1]))
            hfs_python_pkg_dir = "%s/lib/python%i.%i/site-packages" % (
                python_framework_dir, sys.version_info[0], sys.version_info[1])
        else:
            hfs_python_pkg_dir = "$HFS/python/lib/python%i.%i/site-packages" % (
                sys.version_info[0], sys.version_info[1])
        hfs_python_pkg_dir = os.path.expandvars(hfs_python_pkg_dir)
        module_search_path.append(hfs_python_pkg_dir)

    if search_houdini_modules:
        hfs_pkg_dir = "$HFS/houdini/python%i.%ilibs" % (
                sys.version_info[0], sys.version_info[1])
        hfs_pkg_dir = os.path.expandvars(hfs_pkg_dir)
        module_search_path.append(hfs_pkg_dir)

    # Forcefully load the module from $HFS.
    # NOTE: If an older module has already been imported, then Houdini will run
    #       into problems.  The code below will replace the old module with the
    #       good one.  However, there is no way of undoing any of the changes
    #       made by the old module when it was first imported.
    file_name, path_name, description = imp.find_module(
        module_name, module_search_path)
    imp.load_module(module_name, file_name, path_name, description)

    __import__(module_name)

    # Suppress any warnings from pkg_resources.py complaining that the module
    # was imported from $HFS instead from the system folder.  The warning only
    # occurs when Houdini uses the system's Python distro.
    import warnings
    warnings.filterwarnings(
        "ignore",
        message=".*Module " + module_name + " was already imported from.*")
