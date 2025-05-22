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
        self.assertEqual(app.posts[0]['likes'], 0)
        self.assertEqual(app.posts[0]['views'], 0)

    def test_view_post(self):
        """Test viewing an existing post."""
        # Manually add a post for testing this route directly
        app.posts.append({'id': 1, 'title': 'View Me', 'content': 'Content to view', 'likes': 0, 'views': 0})
        app.next_post_id = 2 # Ensure next_post_id is updated

        response1 = self.client.get('/post/1')
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b"View Me", response1.data)
        self.assertIn(b"Content to view", response1.data)
        self.assertIn(b"Views: 1", response1.data) # First view
        self.assertIn(b"Likes: 0", response1.data)

        response2 = self.client.get('/post/1')
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b"Views: 2", response2.data) # Second view
        self.assertIn(b"Likes: 0", response2.data) # Likes should remain unchanged

    def test_view_nonexistent_post(self):
        """Test viewing a post that does not exist."""
        response = self.client.get('/post/999')
        self.assertEqual(response.status_code, 404)

    def test_like_post(self):
        """Test liking a post."""
        # Manually add a post
        app.posts.append({'id': 1, 'title': 'Like Test', 'content': 'Content', 'likes': 0, 'views': 0})
        app.next_post_id = 2

        response = self.client.get('/like_post/1')
        self.assertEqual(response.status_code, 302) # Redirects to post page
        self.assertEqual(response.location, url_for('post', post_id=1, _external=False))
        self.assertEqual(app.posts[0]['likes'], 1)

        response = self.client.get('/like_post/1') # Like again
        self.assertEqual(response.status_code, 302)
        self.assertEqual(app.posts[0]['likes'], 2)

        response = self.client.get('/post/1') # Check the post page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Likes: 2", response.data)

    def test_like_nonexistent_post(self):
        """Test liking a post that does not exist."""
        response = self.client.get('/like_post/999')
        self.assertEqual(response.status_code, 404)

    def test_sorting(self):
        """Test sorting of posts on the index page."""
        # Manually add posts
        app.posts = [
            {'id': 1, 'title': 'Post A', 'content': 'Content A', 'likes': 5, 'views': 10},
            {'id': 2, 'title': 'Post B', 'content': 'Content B', 'likes': 10, 'views': 5},
            {'id': 3, 'title': 'Post C', 'content': 'Content C', 'likes': 2, 'views': 20}
        ]
        app.next_post_id = 4 # Ensure next_post_id is updated

        # Test default sort (by ID)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode()
        self.assertTrue(data.find('Post A') < data.find('Post B') < data.find('Post C'))

        # Test sort by likes
        response = self.client.get('/?sort=likes')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode()
        # Expected order: Post B (10), Post A (5), Post C (2)
        self.assertTrue(data.find('Post B') < data.find('Post A') < data.find('Post C'))

        # Test sort by views
        response = self.client.get('/?sort=views')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode()
        # Expected order: Post C (20), Post A (10), Post B (5)
        self.assertTrue(data.find('Post C') < data.find('Post A') < data.find('Post B'))

if __name__ == "__main__":
    unittest.main()
