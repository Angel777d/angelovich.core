from enum import ReprEnum

from request import HTTPRequest as Request
from response import HTTPResponse as Response
from server import Server

END_OF_LINE: bytes = b'\r\n'


class BytesEnum(bytes, ReprEnum):
	pass


class Protocol(BytesEnum):
	HTTP1_1 = b'HTTP/1.1'
	HTTP2 = b'HTTP/2'


# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
class Code(BytesEnum):
	OK = b'200 OK'
	NOT_FOUND = b'404 Not Found'


# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods
class Method(BytesEnum):
	"""
	Method	Safe	Idempotent	Cacheable
	GET	    Yes	    Yes	        Yes
	HEAD	Yes	    Yes	        Yes
	OPTIONS	Yes	    Yes	        No
	TRACE	Yes	    Yes	        No
	PUT	    No	    Yes	        No
	DELETE	No	    Yes	        No
	POST	No	    No	        Conditional*
	PATCH	No	    No	        Conditional*
	CONNECT	No	    No	        No
	"""

	GET = b'GET'
	HEAD = b'HEAD'
	OPTIONS = b'OPTIONS'
	TRACE = b'TRACE'
	PUT = b'PUT'
	DELETE = b'DELETE'
	POST = b'POST'
	PATCH = b'PATCH'
	CONNECT = b'CONNECT'
