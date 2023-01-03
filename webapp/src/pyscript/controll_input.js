function getUrl(param) {
  console.log(param[0])
  var url = URL.createObjectURL(param[0]);
  console.log(url);
  document.getElementById('preview').src = url;
  return url;
}

function getFile(files) {
  return files[0];
}

function getBase64(file, callback) {
  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function () {
    console.log('file reader load finished')
    const base64String = reader.result
      .replace('data:', '')
      .replace(/^.+,/, '');
    callback(base64String)
  };
  reader.onerror = function (error) {
    console.log('Error: ', error);
  };
}
