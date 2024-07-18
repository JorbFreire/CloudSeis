from bokeh.plotting import curdoc
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from .core import Visualization


def modify_doc(document):
    session_context = document.session_context
    request = session_context.request
    arguments = request.arguments

    file_name = arguments.get('file_name', [b''])[0].decode('utf-8')
    gather_key = arguments.get('gather_key', [b''])[0].decode('utf-8')

    main = Visualization(
        filename=file_name,
        gather_key=gather_key
    )

    # "main_model" could be "main_column"
    document.add_root(main.main_model)


# *** Create a new Bokeh Application
bokeh_app = Application(FunctionHandler(modify_doc))

# *** Run the Bokeh server application
if __name__ == '__main__':
    from bokeh.server.server import Server
    server = Server({'/': bokeh_app}, allow_websocket_origin=["*"])
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
