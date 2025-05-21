import unittest
from app import app, posts # Import app and posts from flask_blog.app

class BlogTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms
        self.client = app.test_client()
        
        # Reset posts and next_post_id before each test for isolation
        app.posts = [] 
        app.next_post_id = 1

    def tearDown(self):
        # Clean up any state if necessary, though setUp handles reset for posts
        pass

    # Test methods will be added here
    def test_index_page(self):
        """Test the index page loads and shows 'No posts yet' initially."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My Blog", response.data)
        self.assertIn(b"No posts yet", response.data)

    def test_create_post(self):
        """Test creating a new post."""
        response = self.client.post('/create', data={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }) # follow_redirects=False by default
        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertEqual(response.location, url_for('index', _external=False)) # Check redirect location

        # Now check the index page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Post", response.data)
        
        self.assertEqual(len(app.posts), 1)
        self.assertEqual(app.posts[0]['title'], 'Test Post')
        self.assertEqual(app.posts[0]['content'], 'This is a test post.')

    def test_view_post(self):
        """Test viewing an existing post."""
        # Manually add a post for testing this route directly
        app.posts.append({'id': 1, 'title': 'View Me', 'content': 'Content to view'})
        app.next_post_id = 2 # Ensure next_post_id is updated

        response = self.client.get('/post/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"View Me", response.data)
        self.assertIn(b"Content to view", response.data)

    def test_view_nonexistent_post(self):
        """Test viewing a post that does not exist."""
        response = self.client.get('/post/999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
