import requests
from os import getenv
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

from .core import Visualization

BASE_URL = getenv(
    'SERVER_URL',
    'http://localhost:5000'
)


def load_file_path(auth_token, workflowId) -> None | str:
    api_url = f"{BASE_URL}/su-file-path/show-path/{workflowId}"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        return None

    absolute_file_path = response.json()["file_path"]
    return absolute_file_path


def modify_document(document):
    session_context = document.session_context
    request = session_context.request
    arguments = request.arguments

    auth_token = request.cookies.get('Authorization', '')
    gather_key = arguments.get('gather_key', [b''])[0].decode('utf-8')
    workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')

    absolute_file_path = load_file_path(
        auth_token=auth_token,
        workflowId=workflowId
    )

    main = Visualization(
        filename=absolute_file_path,
        gather_key=gather_key
    )

    # "main_model" could be "main_column"
    document.add_root(main.main_model)


# *** Create a new Bokeh Application
bokeh_app = Application(FunctionHandler(modify_document))

# *** Run the Bokeh server application
if __name__ == '__main__':
    from bokeh.server.server import Server
    server = Server({'/': bokeh_app}, allow_websocket_origin=["*"])
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
