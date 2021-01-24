from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')

                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            response = client.get('/item/test', headers={'Authorization': self.access_token})

            self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 0.99, 1).save_to_db()
                response = client.get('/item/test_item', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test_item', 'price': 0.99},
                                     json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 0.99, 1).save_to_db()
                response = client.delete('/item/test_item')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.post('/item/test_item', data={'price': 0.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test_item', 'price': 0.99},
                                     json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                client.post('/item/test_item', data={'price': 0.99, 'store_id': 1})
                response = client.post('/item/test_item', data={'price': 0.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test_item\' already exists.'},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.put('/item/test_item', data={'price': 0.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test_item').price, 0.99)
                self.assertDictEqual({'name': 'test_item', 'price': 0.99},
                                     json.loads(response.data))

    def test_put_update_item_(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 1.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test_item').price, 1.99)

                response = client.put('/item/test_item', data={'price': 1.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test_item').price, 1.99)
                self.assertDictEqual({'name': 'test_item', 'price': 1.99},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 1.99, 1).save_to_db()

                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'items': [{'name': 'test_item', 'price': 1.99}]},
                                     json.loads(response.data))
