from pyodide import ffi
import js
import fs
import struct
import base64

def funcToProxy(fileAsB64String):
    mem_fs = fs.open_fs('mem://')
    mem_fs.makedirs('fruit')
    mem_fs.makedirs('vegetables')
    js.console.log('inside the proxy')
    with mem_fs.open('fruit/apple.su', 'wb') as apple:
        bytes_to_save = base64.decodebytes(fileAsB64String.encode())
        print(type(bytes_to_save))
        apple.write(bytes_to_save)

#    with mem_fs.open('fruit/apple.su', 'rb') as file:
#        # Read number of samples (how many values a trace has)
#        file.seek(114)  # change stream position to byte 114
#        bytes_to_unpack = file.read(2)  # read 2 bytes
#        # trace_samples_amount = struct.unpack('<H', bytes_to_unpack)[0]
#        print(bytes_to_unpack)
    pass

print("por enquanto ok!")

function_proxy = ffi.create_once_callable(funcToProxy)

js.getBase64(js.getFile(js.document.getElementById("input-file").files), function_proxy)
