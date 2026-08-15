import unittest
import json
import os
import shutil
from app import app, DATA_FILE, BACKUP_FILE, DATA_DIR, DEFAULT_LINKS, save_links, load_links

class TeslaFullscreenTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Backup existing files if any
        self.temp_backup_data = DATA_FILE + ".unittest_bak"
        self.temp_backup_bak = BACKUP_FILE + ".unittest_bak"

        if os.path.exists(DATA_FILE):
            shutil.copyfile(DATA_FILE, self.temp_backup_data)
        if os.path.exists(BACKUP_FILE):
            shutil.copyfile(BACKUP_FILE, self.temp_backup_bak)

        # Write clean test state
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        if os.path.exists(BACKUP_FILE):
            os.remove(BACKUP_FILE)

    def tearDown(self):
        # Clean up files
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        if os.path.exists(BACKUP_FILE):
            os.remove(BACKUP_FILE)

        # Restore original files
        if os.path.exists(self.temp_backup_data):
            shutil.move(self.temp_backup_data, DATA_FILE)
        if os.path.exists(self.temp_backup_bak):
            shutil.move(self.temp_backup_bak, BACKUP_FILE)

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

        # Check backup file was created and contains the link
        self.assertTrue(os.path.exists(BACKUP_FILE))
        with open(BACKUP_FILE, "r") as f:
            bak_data = json.load(f)
        self.assertEqual(len(bak_data), 1)
        self.assertEqual(bak_data[0]['name'], 'Test Jellyfin')

    def test_add_link_with_existing_protocol(self):
        response = self.app.post('/add', data={
            'name': 'Secure Link',
            'url': 'https://google.com',
            'icon': '🌐'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Secure Link', response.data)
        self.assertIn(b'https://google.com', response.data)

    def test_add_custom_icon(self):
        # When custom icon is selected
        response = self.app.post('/add', data={
            'name': 'Custom Icon Link',
            'url': 'https://example.com',
            'icon': 'custom',
            'custom_icon': '🍿'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Custom Icon Link', response.data)
        self.assertIn('🍿'.encode('utf-8'), response.data)

    def test_edit_link(self):
        # Add two links
        self.app.post('/add', data={'name': 'Alpha', 'url': 'http://alpha.com', 'icon': '🌐'})
        self.app.post('/add', data={'name': 'Beta', 'url': 'http://beta.com', 'icon': '📺'})

        # Edit the first link
        response = self.app.post('/edit/0', data={
            'name': 'Omega',
            'url': 'http://omega.com',
            'icon': '🏠'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Omega', response.data)
        self.assertIn(b'http://omega.com', response.data)
        self.assertNotIn(b'Alpha', response.data)

        # Ensure order/position is maintained
        with open(DATA_FILE, 'r') as f:
            links = json.load(f)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]['name'], 'Omega')
        self.assertEqual(links[1]['name'], 'Beta')

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

    def test_reorder_link(self):
        # Add three links
        self.app.post('/add', data={'name': 'A', 'url': 'http://a.com', 'icon': '🌐'})
        self.app.post('/add', data={'name': 'B', 'url': 'http://b.com', 'icon': '📺'})
        self.app.post('/add', data={'name': 'C', 'url': 'http://c.com', 'icon': '🏠'})

        # Reorder B down (which swaps B and C)
        response = self.app.get('/reorder/1/down', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with open(DATA_FILE, 'r') as f:
            links = json.load(f)
        self.assertEqual(links[0]['name'], 'A')
        self.assertEqual(links[1]['name'], 'C')
        self.assertEqual(links[2]['name'], 'B')

        # Reorder C up (which swaps A and C)
        response = self.app.get('/reorder/1/up', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with open(DATA_FILE, 'r') as f:
            links = json.load(f)
        self.assertEqual(links[0]['name'], 'C')
        self.assertEqual(links[1]['name'], 'A')
        self.assertEqual(links[2]['name'], 'B')

    def test_backup_restore_on_corrupt_data_file(self):
        # Save a valid list first
        valid_links = [{'name': 'Persisted Link', 'url': 'http://example.com', 'icon': '⭐'}]
        save_links(valid_links)

        # Corrupt the main data file
        with open(DATA_FILE, 'w') as f:
            f.write("corrupted json string {")

        # Loading links should recover from backup file
        loaded = load_links()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]['name'], 'Persisted Link')

        # DATA_FILE should have been restored
        with open(DATA_FILE, 'r') as f:
            restored_data = json.load(f)
        self.assertEqual(restored_data[0]['name'], 'Persisted Link')

    def test_fallback_to_defaults_when_both_files_missing_or_corrupted(self):
        # Delete both files
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        if os.path.exists(BACKUP_FILE):
            os.remove(BACKUP_FILE)

        loaded = load_links()
        self.assertEqual(len(loaded), len(DEFAULT_LINKS))
        self.assertEqual(loaded[0]['name'], DEFAULT_LINKS[0]['name'])

        # Both files should be re-created with DEFAULT_LINKS
        self.assertTrue(os.path.exists(DATA_FILE))
        self.assertTrue(os.path.exists(BACKUP_FILE))

if __name__ == '__main__':
    unittest.main()
