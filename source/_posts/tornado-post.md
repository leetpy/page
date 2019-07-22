---
title: tornado 获取提交数据
date: 2018-12-08 13:43:36
categories: python
tags: [tornado]
---

在进行前后台开发时，我们往往需要关注发送/接收数据的类型，不同类型的数据有不同的处理方式。

<!-- more -->

## GET 数据获取

### 获取查询参数

```python
# url: http://localhost/user?username=lina
class ProfileHandler(RequestHandler):
    def get(self):
        username = self.request.query_arguments.get('username', 'default')
```

## POST 数据获取

POST 提交数据有四种方式，分别是 json, 

这里我们使用 postman + tcpdump 分别来发送和抓取http报文。看看不同提交方式，在http里显示是什么样的。

tcpdump 抓包命令：

```
# 这里抓取eth0网口，10000 端口,的报文
sudo tcpdump -i eth0 port 10000 -w data.pcap
```

分别用 postman 发送不同格式的POST请求，然后抓取报文后使用wireshark分析，具体如下：

## json类型

```
POST /api/project/add HTTP/1.1
Content-Type: application/json
cache-control: no-cache
Postman-Token: 833e2732-a7fe-41f2-927a-878462258069
User-Agent: PostmanRuntime/7.4.0
Accept: */*
Host: 127.0.0.1:10000
accept-encoding: gzip, deflate
content-length: 45
Connection: keep-alive

{
    "username": "lina",
    "password": "hello"
}
```


可以看到json的格式比较简单，直接以字典的方式存放在body当中，tornado获取方式如下：

```python
class ProfileHandler(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
```

## x-www-form-urlencoded类型

x-www-form-urlencoded 是默认的form提交方式，数据存放方式和QueryString的方式类似，具体如下：

```
POST /api/project/add HTTP/1.1
Content-Type: application/x-www-form-urlencoded
cache-control: no-cache
Postman-Token: ca8fe418-ca93-48ab-8eed-4545e57ee690
User-Agent: PostmanRuntime/7.4.0
Accept: */*
Host: 127.0.0.1:10000
accept-encoding: gzip, deflate
content-length: 28
Connection: keep-alive

username=lina&password=hello
```
tornado 获取参数方式如下：

```python
class ProfileHandler(RequestHandler):
    def post(self):
        username = self.request.body_arguments.get('username', 'default')

# 或者
class ProfileHandler(RequestHandler):
    def post(self):
        username = self.get_arguement('username', 'default')

```
## form-data类型

```
POST /api/project/add HTTP/1.1
Content-Type: multipart/form-data; boundary=--------------------------296134443182327800498848
cache-control: no-cache
Postman-Token: e013cd04-567a-42a2-b72a-10b70f5d7d4f
User-Agent: PostmanRuntime/7.4.0
Accept: */*
Host: 127.0.0.1:10000
accept-encoding: gzip, deflate
content-length: 279
Connection: keep-alive

----------------------------296134443182327800498848
Content-Disposition: form-data; name="username"

lina
----------------------------296134443182327800498848
Content-Disposition: form-data; name="password"

hello
----------------------------296134443182327800498848--
```

multipart/form-data类型的数据会生成boundary,用于分割不同字段，以避免正文内容重复。

使用 python 发送multipart/form-data数据比较麻烦，可以使用`requests-toolbelt`库。

```python
from requests_toolbelt import MultipartEncoder
from webob import Request
import io

# Create a buffer object that can be read by the MultipartEncoder class
# This works just like an open file object
file = io.BytesIO()

# The file content will be simple for my test.
# But you could just as easily have a multi-megabyte mpg file
# Write the contents to the file
file.write(b'test mpg content')

# Then seek to the beginning of the file so that the
# MultipartEncoder can read it from the beginning
file.seek(0)

# Create the payload
payload = MultipartEncoder(
    {

        # The name of the file upload field... Not the file name
        'uploadedFile': (

            # This would be the name of the file
            'This is my file.mpg',

            # The file handle that is ready to be read from
            file,

            # The content type of the file
            'application/octet-stream'
        )
    }

# To send the file, you would use the requests.post method
# But the content type is not application-octet-stream
# The content type is multipart/form-data; with a boundary string
# Without the proper header type, your server would not be able to
# figure out where the file begins and ends and would think the
# entire post content is the file, which it is not. The post content
# might even contain multiple files
# So, to send your file, you would use:
#
# response = requests.post(url, data=payload, headers={'Content-Type': payload.content_type})

# Instead of sending the payload to the server,
# I am just going to grab the output as it would be sent
# This is because I don't have a server, but I can easily
# re-create the object using this output
postData = payload.to_string()

# Create an input buffer object
# This will be read by our server (our webob.Request object)
inputBuffer = io.BytesIO()

# Write the post data to the input buffer so that the webob.Request object can read it
inputBuffer.write(postData)

# And, once again, seek to 0
inputBuffer.seek(0)

# Create an error buffer so that errors can be written to it if there are any
errorBuffer = io.BytesIO()

# Setup our wsgi environment just like the server would give us
environment = {
    'HTTP_HOST': 'localhost:80',
    'PATH_INFO': '/index.py',
    'QUERY_STRING': '',
    'REQUEST_METHOD': 'POST',
    'SCRIPT_NAME': '',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '80',
    'SERVER_PROTOCOL': 'HTTP/1.0',
    'CONTENT_TYPE': payload.content_type,
    'wsgi.errors': errorBuffer,
    'wsgi.input': inputBuffer,
    'wsgi.multiprocess': False,
    'wsgi.multithread': False,
    'wsgi.run_once': False,
    'wsgi.url_scheme': 'http',
    'wsgi.version': (1, 0)
}

# Create our request object
# This is the same as your request object and should have all our info for reading
# the file content as well as the file name
request = Request(environment)

# At this point, the request object is the same as what you get on your server
# So, from this point on, you can use the following code to get
# your actual file content as well as your file name from the object

# Our uploaded file is in the POST. And the POST field name is 'uploadedFile'
# Grab our file so that it can be read
uploadedFile = request.POST['uploadedFile']

# To read our content, you can use uploadedFile.file.read()
print(uploadedFile.file.read())

# And to get the file name, you can use uploadedFile.filename
print(uploadedFile.filename)
```

## text/xml
