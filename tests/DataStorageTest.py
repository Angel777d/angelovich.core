import unittest

from angelovichcore.DataStorage import DataStorage


class DataStorageTestCase(unittest.TestCase):
	def test_entity_create(self):
		ds = DataStorage()
		entity = ds.create_entity()
		assert entity is not None
		assert entity.is_valid()

		ds.remove_entity(entity)
		assert not entity.is_valid()


if __name__ == '__main__':
	unittest.main()
