from models.store import StoreModel
from models.item import ItemModel

from tests.base_test import BaseTest


class TestStore(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [],
                             "The store's items length was not 0 even though no items were added.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'),
                              f"Found a store with the name '{store.name}' in the database even though it wasn't yet written.")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'),
                                 f"Didn't found a store with the name '{store.name}' in the database even though it was written.")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'),
                              f"Found a store with the name '{store.name}' in from the database even though it was deleted.")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 0.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test item')

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'id': None,
            'name': 'test',
            'items': []
        }

        self.assertDictEqual(expected, store.json(),
                             f"The JSON export of the store is incorrect. Expected {expected}, received {store.json()}.")


    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 0.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'id': 1,
                'name': 'test',
                'items': [{'name': 'test item', 'price': 0.99}]
            }

            self.assertDictEqual(expected, store.json(),
                                 f"The JSON export of the store is incorrect. Expected {expected}, received {store.json()}.")
