import os

from bookish.flaskapp import app, configure_app

from houdinihelp.hconfig import HoudiniDevConfig, HoudiniAppConfig

try:
    import hou
except ImportError:
    hou = None


def is_dev():
    return "SHH" in os.environ


def get_houdini_app(dev=None, config_file=None, config_obj=None, **kwargs):
    # If dev is None, that means try to detect the environment
    if dev is None:
        dev = is_dev()

    # Choose a different config class based on dev
    if not config_obj:
        config_obj = HoudiniDevConfig if dev else HoudiniAppConfig

    # If the caller didn't specify an explict config file, and hou is availabe,
    # use findFile to find a config file in the Houdini path
    if not config_file and hou:
        try:
            config_file = hou.findFile("config/Help/bookish.cfg")
        except hou.OperationFailed:
            pass

    configure_app(config_obj=config_obj, config_file=config_file, **kwargs)
    return app


def start_server(host="0.0.0.0", port=8080, debug=False, bgindex=None,
                 config_file=None, dev=None, **kwargs):
    app = get_houdini_app(dev=dev, config_file=config_file)
    if bgindex is not None:
        app.config["ENABLE_BACKGROUND_INDEXING"] = bgindex
    return app.run(host=host, port=port, debug=debug, **kwargs)


def start_dev_server(host="0.0.0.0", port=8080, debug=None, bgindex=None,
                     **kwargs):
    return start_server(host, port, debug, bgindex, dev=True, **kwargs)


def start_app_server(host="0.0.0.0", port=48626, debug=None, bgindex=None,
                     **kwargs):
    return start_server(host, port, debug, bgindex, dev=False, **kwargs)


if __name__ == "__main__":
    start_dev_server(debug=True, bgindex=True)
