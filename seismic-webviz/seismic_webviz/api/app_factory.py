import requests
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.document.document import Document


from ..core import Visualization
from .config import BASE_URL


def app_factory():
    def find_file_path(auth_token: str, workflowId: int) -> None | str:
        api_url = f"{BASE_URL}/su-file-path/show-path/{workflowId}"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            return None

        absolute_file_path = response.json()["file_path"]
        return absolute_file_path

    def modify_document(document: Document) -> None:
        session_context = document.session_context
        request = session_context.request
        arguments = request.arguments

        auth_token = request.cookies.get('Authorization', '')
        gather_key = arguments.get('gather_key', [b''])[0].decode('utf-8')
        workflowId = arguments.get('workflowId', [b''])[0].decode('utf-8')

        absolute_file_path = find_file_path(
            auth_token=auth_token,
            workflowId=int(workflowId)
        )

        visualization_manager = Visualization(
            filename=absolute_file_path,
            gather_key=gather_key
        )

        document.add_root(visualization_manager.root_layout)

    # *** Create a new Bokeh Application
    bokeh_app = Application(FunctionHandler(func=modify_document))

    return bokeh_app