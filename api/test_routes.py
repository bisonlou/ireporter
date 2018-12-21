import unittest
import json
from api.routes import app, red_flags


class TestRoutes(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = app.test_client()

    def tearDown(self):
        """
        teardown test client
        """
        red_flags.clear()    
        
    def test_add_red_flag(self):
        """
        Test adding a red flag with expected details
        """
        red_flag = {
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'description': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }

        response = self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag)
        )

        message = json.loads(response.data)
        print(message['data'][0]['message'])
        self.assertEqual(message['status'], 201)  
        self.assertEqual(message['data'][0]['message'], 'Created red-flag record')  
        assert(len(red_flags) > 0)

    def test_get_all_red_flags(self):
        """
        Test getting all red flags
        """
        red_flag1 = {
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'description': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }

        red_flag2 = {
            'date': '2018-12-12',
            'offender': 'Magistrate',
            'description': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }

        self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag1)
        )

        self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag2)
        )

        response = self.test_client.get(
            '/api/v1/redflags')

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        assert(len(red_flags) > 0)
        assert(len(red_flags) == 2)    

    def test_update_red_flags_location(self):
        """
        Test updateing a redflags location
        """
        red_flag = {
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'description': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }
        
        self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag)
        )

        response = self.test_client.patch(
            '/api/v1/redflag/1/(0.000000, 0.000000)')

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertTrue(len(red_flags) == 1)
        self.assertEqual(
            (message['data'][0]['message']),
            'Updated red-flag record’s location')
        self.assertEqual((message['data'][0]['id']), 1)
        self.assertEquals(red_flags[0]['location'], '(0.000000, 0.000000)')