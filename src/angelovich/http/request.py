from asyncio import StreamReader
from dataclasses import dataclass
from urllib.parse import parse_qs
from urllib.parse import urlparse

from angelovich.http import Method, Protocol, END_OF_LINE


@dataclass(frozen=True)
class HTTPRequest:
	method: Method
	path: str
	args: dict[str, list[str]]
	protocol: Protocol
	headers: dict[str, str]
	body: bytes

	@staticmethod
	async def read(reader: StreamReader) -> "HTTPRequest":

		# start line
		method, path, protocol = (await reader.readline()).strip(END_OF_LINE).split(b' ')
		method = Method(method)
		protocol = Protocol(protocol)

		path = path.decode('latin-1')
		parsed_url = urlparse(path)
		path = parsed_url.path
		args = parse_qs(parsed_url.query)

		headers = {}
		line = await reader.readline()
		while line != END_OF_LINE:
			key, value = line.strip(END_OF_LINE).decode('latin-1').split(": ")
			headers[key] = value
			line = await reader.readline()

		body = bytes()
		if "Content-Length" in headers:
			length = int(headers["Content-Length"])
			body = await reader.readexactly(length)

		return HTTPRequest(method, path, args, protocol, headers, body)
