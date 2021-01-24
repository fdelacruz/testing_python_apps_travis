from tests.unit.unit_base_test import UnitBaseTest

from models.item import ItemModel


class TestItem(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('test', 0.99, 1)

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 0.99,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store, "The item's store was not None even though the store was not created.")

    def test_item_json(self):
        item = ItemModel('test', 0.99, 1)

        expected = {
            'name': item.name,
            'price': 0.99
        }

        self.assertEqual(expected, item.json(), "The JSON export of the item is incorrect. Expected {}, received {}.".format(expected, item.json()))
