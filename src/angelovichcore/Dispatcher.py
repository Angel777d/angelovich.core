from typing import Callable, Hashable, Dict, List, Tuple, Awaitable

CallbackType = Callable[[...], Awaitable[...]]
class Dispatcher:
	def __init__(self):
		self.__handlers: Dict[str, List[Tuple[Hashable, CallbackType]]] = {}

	def add_listener(self, event: str, callback: CallbackType, scope: Hashable = None) -> None:
		self.__handlers.setdefault(event, []).append((scope, callback))

	def remove_listener(self, event: str, scope: Hashable = None) -> None:
		self.__handlers[event] = [(s, c) for s, c in self.__handlers.get(event, []) if s != scope]

	def remove_all(self, scope: Hashable) -> None:
		for event, handlers in self.__handlers.items():
			self.__handlers[event] = [(s, c) for s, c in handlers if s != scope]

	async def dispatch(self, event: str, *args, **kwargs) -> None:
		for e, callback in self.__handlers.get(event, []):
			await callback(*args, **kwargs)
