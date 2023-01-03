def add_one():
    Element("output").write(str(global_vars['internalCounter']))
    global_vars['internalCounter'] += 1

def log_file():
    import js
    import urllib3
    Element("output").write("input changed")
    js.console.log(
        # js.URL.createObjectURL(
            js.document.getElementById("input-file").files
        # )
    )
    url = js.getUrl(js.document.getElementById("input-file").files)
    http = urllib3.PoolManager()

    content = http.request('GET', url)
    js.console.log("url on python:")
    js.console.log(url)
    # result = readsu(content)
    js.console.log(content)
