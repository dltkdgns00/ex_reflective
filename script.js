var _ = function (id) { return document.getElementById(id); } // getElementById

var POST = function (api, data, func) // POST request
{
  var request = new XMLHttpRequest();
  request.onreadystatechange = function ()
  {
    if (request.readyState == 4)
    {
      var resp = ""
      try
      {
        if (request.response[0] == '<')
        {
          var resp = {
            status: 'error',
            data: 'Unknown error : ['
              + request.responseText + ']'
          };
        } else
        {
          resp = JSON.parse(request.response);
        }
      } catch (e)
      {
        resp = {
          status: 'error',
          data: 'Unknown error : ['
            + request.responseText + ']'
        };
        alert(request.responseText)
      }
      func(resp)
    }
  };
  request.open('POST', api);
  request.send(data);
  return request
}

var API_post = "/www" // Apache2 또는 Nginx 서버에서 설정한 경로
function postFunc() // POST 요청
{
  var data = new FormData();
  data.append('func', _('func').value);

  POST(API_post, data, function (resp)
  {
    if (resp.data)
      _('response_msg').innerHTML = JSON.stringify(resp.data)
    else
      alert("no message")
  });
};

document.addEventListener("DOMContentLoaded", function () // 페이지가 로드되면 웹소켓 서버 연결
{
  var ws = new WebSocket('ws://localhost:5000');

  ws.onopen = function ()
  {
    console.log('Connected to the server');
    ws.send('Hello, server!');
  };

  ws.onmessage = function (event)
  {
    console.log('Received message: ' + event.data);
  };

  ws.onerror = function (error)
  {
    console.log('WebSocket error: ' + error.message);
  };

  ws.onclose = function (event)
  {
    console.log('WebSocket connection closed: ' + event.code);
  };
})
