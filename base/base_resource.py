

class BaseResource(object):
    def __init__(self):
        self._prefix = None

    def api_register(self, app):
        for attr in dir(self):
            attr = getattr(self, attr)
            if hasattr(attr, "__name__"):
                func_name = attr.__name__
                method = func_name.split("_")[0].upper()
                if method in ("GET", "POST"):
                    try:
                        endpoint = "_".join(func_name.split("_")[1:])
                    except:
                        endpoint = ""
                    print("adding", "/"+self._prefix+"/"+endpoint, "methods:", method)
                    app.add_url_rule("/"+self._prefix+"/"+endpoint, view_func=attr, methods=[method])

