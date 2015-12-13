import nose
from houdinihelp import api


def test_node_template():
    api.initialize()
    text = api.nodeHelpTemplate("Object", "foo", "bar", "1.0")
    assert text
