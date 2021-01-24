from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class TestItem(BaseTest):
    def test_crud(self):
        with self.app_context():
            item = ItemModel('test', 0.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              f"Found an item with name {item.name}, but expected not too.")

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test store')
            item = ItemModel('test', 0.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test store')
