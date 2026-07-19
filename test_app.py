import unittest
import json
import os
import shutil
from app import app, DATA_FILE, DATA_DIR

class TeslaFullscreenTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Backup existing links.json if any
        self.backup_path = DATA_FILE + ".bak"
        if os.path.exists(DATA_FILE):
            shutil.copyfile(DATA_FILE, self.backup_path)

        # Write clean test state
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    def tearDown(self):
        # Restore backup if any
        if os.path.exists(self.backup_path):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            shutil.move(self.backup_path, DATA_FILE)
        elif os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_dashboard_empty(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No links added yet', response.data)

    def test_add_link(self):
        response = self.app.post('/add', data={
            'name': 'Test Jellyfin',
            'url': '192.168.1.50:8096',
            'icon': '📺'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Jellyfin', response.data)
        self.assertIn(b'http://192.168.1.50:8096', response.data)
        self.assertIn('📺'.encode('utf-8'), response.data)

    def test_add_link_with_existing_protocol(self):
        response = self.app.post('/add', data={
            'name': 'Secure Link',
            'url': 'https://google.com',
            'icon': '🌐'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Secure Link', response.data)
        self.assertIn(b'https://google.com', response.data)

    def test_delete_link(self):
        self.app.post('/add', data={
            'name': 'Delete Me',
            'url': '192.168.1.50:8096',
            'icon': '📺'
        })

        response = self.app.get('/')
        self.assertIn(b'Delete Me', response.data)

        response = self.app.get('/delete/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Delete Me', response.data)

if __name__ == '__main__':
    unittest.main()
