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
				return self.value.__hash__()

		ds = DataStorage()
		ds.create_entity().add_component(TestComponent(1))
		ds.create_entity().add_component(TestComponent(2))
		collection = ds.get_collection(TestComponent)

		assert len(collection) == 2
		assert collection.find(1) is not None
		assert collection.find(2) is not None
		assert collection.find(3) is None


if __name__ == '__main__':
	unittest.main()
