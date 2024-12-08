import unittest
from app import create_app
import json

class TestNotesAPI(unittest.TestCase):

    def setUp(self):
        """Set up the app and client for testing."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_note_valid(self):
        """Test creating a note with valid data."""
        response = self.client.post('/api/notes', json={'title': 'Test Note', 'content': 'This is a test note'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Note', response.get_data(as_text=True))

    def test_create_note_missing_title(self):
        """Test creating a note with missing title."""
        response = self.client.post('/api/notes', json={'content': 'This is a test note'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.get_data(as_text=True))

    def test_create_note_empty_title(self):
        """Test creating a note with an empty title."""
        response = self.client.post('/api/notes', json={'title': '', 'content': 'This is a test note'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.get_data(as_text=True))

    def test_create_note_missing_content(self):
        """Test creating a note with missing content."""
        response = self.client.post('/api/notes', json={'title': 'Test Note'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('content', response.get_data(as_text=True))

    def test_create_note_empty_content(self):
        """Test creating a note with empty content."""
        response = self.client.post('/api/notes', json={'title': 'Test Note', 'content': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('content', response.get_data(as_text=True))

    def test_get_notes(self):
        """Test retrieving all notes."""
        self.client.post('/api/notes', json={'title': 'Test Note', 'content': 'This is a test note'})
        response = self.client.get('/api/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Note', response.get_data(as_text=True))

    def test_get_note_not_found(self):
        """Test getting a note that does not exist."""
        response = self.client.get('/api/notes/999')
        self.assertEqual(response.status_code, 404)

    def test_update_note(self):
        """Test updating a note (with both fields updated)."""
        response = self.client.post('/api/notes', json={'title': 'Old Title', 'content': 'Old Content'})
        note_id = json.loads(response.get_data(as_text=True))['id']
        response = self.client.put(f'/api/notes/{note_id}', json={'title': 'Updated Title', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Title', response.get_data(as_text=True))

    def test_update_note_partial(self):
        """Test updating a note (with only one field updated)."""
        response = self.client.post('/api/notes', json={'title': 'Old Title', 'content': 'Old Content'})
        note_id = json.loads(response.get_data(as_text=True))['id']
        response = self.client.put(f'/api/notes/{note_id}', json={'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Title', response.get_data(as_text=True))

        # Check that content wasn't changed
        response = self.client.get(f'/api/notes/{note_id}')
        self.assertIn('Old Content', response.get_data(as_text=True))

    def test_delete_note(self):
        """Test deleting a note."""
        response = self.client.post('/api/notes', json={'title': 'To Delete', 'content': 'Delete me'})
        note_id = json.loads(response.get_data(as_text=True))['id']
        response = self.client.delete(f'/api/notes/{note_id}')
        self.assertEqual(response.status_code, 200)

    def test_update_note_missing_title(self):
        """Test updating a note with missing title."""
        response = self.client.post('/api/notes', json={'title': 'Old Title', 'content': 'Old Content'})
        note_id = json.loads(response.get_data(as_text=True))['id']
        response = self.client.put(f'/api/notes/{note_id}', json={'content': 'Updated Content'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Content', response.get_data(as_text=True))

    def test_update_note_empty_title(self):
        """Test updating a note with an empty title."""
        response = self.client.post('/api/notes', json={'title': 'Old Title', 'content': 'Old Content'})
        note_id = json.loads(response.get_data(as_text=True))['id']
        response = self.client.put(f'/api/notes/{note_id}', json={'title': '', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.get_data(as_text=True))

    def test_update_note_missing_content(self):
        """Test updating a note with missing content."""
        response = self.client.post('/api/notes', json={'title': 'Old Title', 'content': 'Old Content'})
        note_id = json.loads(response.get_data(as_text=True))['id']
        response = self.client.put(f'/api/notes/{note_id}', json={'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Title', response.get_data(as_text=True))

    def test_update_note_empty_content(self):
        """Test updating a note with empty content."""
        response = self.client.post('/api/notes', json={'title': 'Old Title', 'content': 'Old Content'})
        note_id = json.loads(response.get_data(as_text=True))['id']
        response = self.client.put(f'/api/notes/{note_id}', json={'title': 'Updated Title', 'content': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('content', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
