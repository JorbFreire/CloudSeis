from pyodide import ffi
import js
import fs

def funcToProxy(fileAsB64String):
    mem_fs = fs.open_fs('mem://')
    mem_fs.makedirs('fruit')
    mem_fs.makedirs('vegetables')
    js.console.log('inside the proxy')
    with mem_fs.open('fruit/apple.su', 'w') as apple:
        apple.write(fileAsB64String)

    with mem_fs.open('fruit/apple.su') as apple:
        result = apple.read()
        js.console.log(result[0:50])
    pass

print("por enquanto ok!")

function_proxy = ffi.create_once_callable(funcToProxy)

js.getBase64(js.getFile(js.document.getElementById("input-file").files), function_proxy)
