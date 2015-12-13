import re
from datetime import datetime

from bookish import compat, paths, stores, wikipages

from houdinihelp import api


class HoudiniStore(stores.OverlayStore):
    def __init__(self):
        import hou

        # Help stored in node Help tabs and tool Help tabs
        self.stores = [AssetStore(), ShelfStore()]


class AssetStore(stores.StringStore):
    """A provider which translates requests for help under /nodes/ into calls
    to HOM to load embedded help content from digital assets.
    """

    @staticmethod
    def _find_all_assets():
        import hou

        for path in hou.hda.loadedFiles():
            # List of hou.HDADefinition objects
            hdadefs = hou.hda.definitionsInFile(path)
            for hdadef in hdadefs:
                yield hdadef

    @staticmethod
    def _asset_is_hidden(hdadef):
        # Ignore assets that are maked "hidden" or that are not the current
        # definition
        return (not hdadef.isCurrent()) or hdadef.nodeType().hidden()

    @staticmethod
    def _get_hdadef(table, scopeop, ns, name, version):
        import hou

        # HOM doesn't like unicode :(
        scopeop = str(scopeop) if scopeop else None
        ns = str(ns) if ns else None
        name = str(name)
        version = str(version) if version else ''

        fullname = hou.hda.fullNodeTypeNameFromComponents(
            scopeop, ns, name, version
        )
        type_cat = hou.nodeTypeCategories()[table]
        nodetype = hou.nodeType(type_cat, str(fullname))
        if nodetype:
            return nodetype.definition()

    @staticmethod
    def _path_to_hdadef(path):
        nodetype = api.path_to_nodetype(path)
        if nodetype:
            return nodetype.definition()

    def exists(self, path):
        nodetype = api.path_to_nodetype(path)
        if nodetype and not nodetype.hidden():
            hdadef = nodetype.definition()
            info = api.path_to_components(path)
            if hdadef:
                return (
                    (path.endswith(".txt") and hdadef.embeddedHelp()) or
                    (info.section and info.section in hdadef.section())
                )

    def list_all(self, path="/"):
        for hdadef in self._find_all_assets():
            if hdadef.embeddedHelp() and not self._asset_is_hidden(hdadef):
                nodepath = api.nodetype_to_path(hdadef.nodeType())
                if nodepath.startswith(path):
                    yield nodepath + ".txt"

    def last_modified(self, path):
        hdadef = self._path_to_hdadef(path)
        if hdadef:
            timestamp = hdadef.modificationTime()
            return datetime.utcfromtimestamp(timestamp)
        else:
            raise stores.ResourceNotFoundError(path)

    def writable(self, path):
        hdadef = self._path_to_hdadef(path)
        return bool(hdadef)

    def write_file(self, path, bytestring):
        nodetype = api.path_to_nodetype(path)
        if nodetype:
            hdadef = nodetype.definition()
            if not hdadef:
                raise Exception("%r is not an asset" % path)

            info = api.path_to_components(path)
            sections = hdadef.sections()
            section = info.section or "Help"
            if section in sections:
                sections[section].setContents(bytestring)
            else:
                hdadef.addSection(section, bytestring)

    def delete(self, path):
        nodetype = api.path_to_nodetype(path)
        if nodetype:
            hdadef = nodetype.definition()
            if not hdadef:
                raise Exception("%r is not an asset" % path)

            info = api.path_to_components(path)
            section = info.section or "Help"
            if hdadef:
                hdadef.sections()[section].setContents("")

    def content(self, path, encoding="utf8"):
        hdadef = self._path_to_hdadef(path)
        if not hdadef or self._asset_is_hidden(hdadef):
            raise stores.ResourceNotFoundError(path)
        info = api.path_to_components(path)

        if info.section:
            content = hdadef.sections()[info.section].contents()
        else:
            content = hdadef.embeddedHelp()

        if encoding and isinstance(content, compat.bytes_type):
            content = content.decode(encoding)

        return content

    def is_dir(self, path):
        return False

    def etag(self, path):
        import hou

        hdadef = self._path_to_hdadef(path)
        if hdadef:
            return str(hdadef.modificationTime())


class ShelfStore(stores.StringStore):
    """
    A provider which translates requests for help under /shelf/ into calls
    to HOM to load embedded help content from shelf tools.
    """

    nodeexp = re.compile("/shelf/(.*)")

    def __init__(self):
        super(ShelfStore, self).__init__()

    def _path_to_tool(self, path):
        import hou

        match = self.nodeexp.match(path)
        if match:
            base, ext = paths.split_extension(match.group(1))
            return hou.shelves.tool(base)

    def list_dir(self, path):
        if path == "/shelf/":
            import hou
            return sorted(hou.shelves.tools())
        else:
            return ()

    def exists(self, path):
       return bool(self._path_to_tool(path))

    def content(self, path, encoding="utf8"):
        tool = self._path_to_tool(path)
        if tool:
            bytestring = tool.help()
            if encoding:
                return bytestring.decode(encoding)
            else:
                return bytestring
        else:
            raise stores.ResourceNotFoundError(path)

    def write_file(self, path, bytestring):
        tool = self._path_to_tool(path)
        if tool:
            tool.setHelp(bytestring)
        else:
            raise stores.ResourceNotFoundError(path)

    def delete(self, path):
        self.write_file(path, b"")

    def is_dir(self, path):
        return False

