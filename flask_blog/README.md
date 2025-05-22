# Flask Blog Application

## Description
A simple blog application built with Flask that allows users to create, view, and interact with blog posts. It features post views, likes, and sorting functionalities, all styled with Tailwind CSS.

## Features
*   Create blog posts with a title and content.
*   View a list of all created blog posts on the homepage.
*   View individual blog posts on their own pages.
*   Tracks and displays the number of views for each post.
*   Allows users to "like" posts and displays the total like count.
*   Sort posts on the index page:
    *   By default (post ID, chronological)
    *   By most liked
    *   By most viewed
*   Clean and modern UI styled with Tailwind CSS.

## Project Structure
*   **`app.py`**: The main Flask application file. It contains all the routes, view functions, and core logic for the blog.
*   **`templates/`**: This directory holds all the HTML templates used by the application.
    *   `base.html`: The base template that other templates extend. It includes the main HTML structure, navigation, and footer.
    *   `index.html`: Template for the homepage, displaying a list of all blog posts and sorting options.
    *   `post.html`: Template for displaying a single blog post, including its content, views, and likes.
    *   `create_post.html`: Template containing the form for creating new blog posts.
*   **`test_app.py`**: Contains unit tests for the application's functionalities.
*   **`README.md`**: This file, providing information about the project.

## Setup and Running the Application

### 1. Create a Virtual Environment (Recommended)
It's good practice to use a virtual environment to manage project dependencies.
```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
The primary dependency is Flask.
```bash
pip install Flask
```

### 3. Run the Application
Once Flask is installed, you can run the application:
```bash
python app.py
```
The application will typically be available at `http://127.0.0.1:5000/` in your web browser.

### 4. Run Unit Tests
To run the unit tests:
```bash
python test_app.py
```

## Styling
The application is styled using [Tailwind CSS](https://tailwindcss.com/) via the Play CDN. This allows for rapid UI development with utility classes directly in the HTML templates, without needing a local CSS build step for this simple project. All styling is handled within the `templates/*.html` files using Tailwind's class system.

---
*This is a sample project, and data is stored in-memory, meaning it will be lost when the application server is restarted.*
