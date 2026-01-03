from asyncio import StreamWriter
from dataclasses import dataclass
from typing import List

from angelovich.http import Code, Protocol, END_OF_LINE


@dataclass
class HTTPResponse:
	protocol: Protocol
	code: Code
	headers: List[str]
	body: bytes

	def send(self, writer: StreamWriter):
		# start line
		writer.write(self.protocol)
		writer.write(b' ')
		writer.write(self.code)
		writer.write(END_OF_LINE)

		# headers
		for header in self.headers:
			writer.write(f"{header}\r\n".encode("ascii"))

		# content
		if self.body:
			writer.write(f'Content-Length: {len(self.body)}\r\n'.encode())
			writer.write(END_OF_LINE)
			writer.write(self.body)
