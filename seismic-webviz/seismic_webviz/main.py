from bokeh.plotting import curdoc
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from .core import Visualization


def on_session_created(session_context):
    print("New session created!")
    suFileName = session_context.request.arguments["file_name"][0].decode('UTF-8')
    print("suFileName:")
    print(suFileName)
    
    main = Visualization(
        filename=suFileName,
    )

    document = curdoc()
    # "main_model" could be "main_column"
    document.add_root(main.main_model)


# Create a new Bokeh Application
bokeh_app = Application(FunctionHandler(on_session_created))

# Run the Bokeh server application
if __name__ == '__main__':
    from bokeh.server.server import Server
    server = Server({'/': bokeh_app}, allow_websocket_origin=["*"])
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()