import unittest

from angelovich.core.DataStorage import DataStorage, EntityComponent


class DataStorageTestCase(unittest.TestCase):
	def test_entity_create(self):
		ds = DataStorage()
		entity = ds.create_entity()
		assert entity is not None
		assert entity.is_valid()

		ds.remove_entity(entity)
		assert not entity.is_valid()

	def test_hash_collection(self):
		class TestComponent(EntityComponent):
			def __init__(self, value: int = 0):
				super().__init__()
				self.value: int = value

			def __hash__(self):
				return hash(self.value)

		class TestComponent2(EntityComponent):
			def __init__(self, value: int = 0, value2: str = ""):
				super().__init__()
				self.value1: int = value
				self.value2: str = value2

			@staticmethod
			def make_key(k1: int, k2: str):
				return k1, k2

			def __hash__(self):
				return hash(self.make_key(self.value1, self.value2))

		ds = DataStorage()
		ds.create_entity().add_component(TestComponent(1))
		ds.create_entity().add_component(TestComponent(2))
		collection = ds.get_collection(TestComponent)

		assert len(collection) == 2
		assert collection.find(1) is not None
		assert collection.find(2) is not None
		assert collection.find(3) is None

		ds.create_entity().add_component(TestComponent2(1, "dasda"))
		ds.create_entity().add_component(TestComponent2(2, "asdasda"))
		collection = ds.get_collection(TestComponent2)
		assert len(collection) == 2
		assert collection.find(TestComponent2.make_key(1, "dasda")) is not None
		assert collection.find(TestComponent2.make_key(2, "asdasda")) is not None
		assert collection.find(TestComponent2.make_key(2, "ddd")) is None
		assert collection.find(TestComponent2.make_key(1, "ddd")) is None


if __name__ == '__main__':
	unittest.main()
