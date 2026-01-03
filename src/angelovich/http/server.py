import asyncio
import logging
from asyncio import Server as AsyncServer
from asyncio import StreamReader, StreamWriter
from typing import Dict, Optional, Tuple

from angelovich.http import Code, Protocol, Method, Request, Response

logger = logging.getLogger(__name__)


class Handler:
	async def on_request(self, path: str, request: Request) -> Response:
		raise NotImplementedError


class ErrorHandler(Handler):
	async def on_request(self, path: str, request: Request) -> Response:
		headers = ["Content-Type: text/html; charset=utf-8"]
		return Response(
			Protocol.HTTP1_1,
			Code.NOT_FOUND,
			headers,
			"Page Not Found".encode()
		)


class Server:
	def __init__(self):
		self.handlers: Dict[Method, Dict[str, Handler]] = {}
		self.error_handler: Handler = ErrorHandler()

		self.server: Optional[AsyncServer] = None

	def add_handler(self, method: Method, path: str, handler: Handler):
		self.handlers.setdefault(method, {})[path] = handler

	def select_handler(self, request: Request) -> Tuple[str, Handler]:
		for method in self.handlers:
			if request.method != method:
				continue

			handlers = self.handlers[method]
			path_list = sorted(path for path in handlers if request.path.startswith(path))
			if path_list:
				path = path_list[-1]
				relative_path = request.path[len(path):]
				return relative_path, handlers[path]
		return "", self.error_handler

	async def run(self, host: str, port: int):
		self.server = await asyncio.start_server(self.on_request, host, port)

	def stop(self):
		self.server.close()

	async def on_request(self, reader: StreamReader, writer: StreamWriter):
		request = await Request.read(reader)
		logger.debug(f"Request: {request}")

		path, handler = self.select_handler(request)
		response = await handler.on_request(path, request)
		logger.debug(f"Response: {response}")

		response.send(writer)
