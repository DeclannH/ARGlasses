# repairs/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from pymongo import MongoClient
from bson import ObjectId
import json

class RepairAPITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.mongo_client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.mongo_client['your_database_name']
        cls.repairs_collection = cls.db['repairs']

    def setUp(self):
        self.repair_id = self.repairs_collection.insert_one({
            'vehicle': 'Sample Vehicle',
            'status': 'pending',
            'steps': []
        }).inserted_id

    def tearDown(self):
        self.repairs_collection.delete_many({})

    def test_update_repair_status(self):
        response = self.client.patch(
            reverse('update_repair', kwargs={'repair_id': str(self.repair_id)}),
            data=json.dumps({'status': 'in progress'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Repair updated successfully', response.json()['message'])

        repair = self.repairs_collection.find_one({'_id': ObjectId(self.repair_id)})
        self.assertEqual(repair['status'], 'in progress')

    def test_update_repair_steps(self):
        response = self.client.patch(
            reverse('update_repair', kwargs={'repair_id': str(self.repair_id)}),
            data=json.dumps({'steps': ['Step 1', 'Step 2']}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Repair updated successfully', response.json()['message'])

        repair = self.repairs_collection.find_one({'_id': ObjectId(self.repair_id)})
        self.assertEqual(repair['steps'], ['Step 1', 'Step 2'])

    def test_update_repair_not_found(self):
        response = self.client.patch(
            reverse('update_repair', kwargs={'repair_id': '60f7f6fd2ab79c8b3c8a9e2d'}),
            data=json.dumps({'status': 'completed'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('Repair not found', response.json()['error'])
