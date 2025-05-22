from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Temporary in-memory list to store blog posts
posts = []
next_post_id = 1

@app.route('/')
def index():
    sort_by = request.args.get('sort')
    
    # Make a copy of the posts list to sort
    sorted_posts = list(posts) 

    if sort_by == 'likes':
        sorted_posts.sort(key=lambda p: p['likes'], reverse=True)
    elif sort_by == 'views':
        sorted_posts.sort(key=lambda p: p['views'], reverse=True)
    else: # Default sort by ID (creation time)
        sorted_posts.sort(key=lambda p: p['id'])
        sort_by = None # To correctly highlight 'Default' if no valid sort_by is given

    return render_template('index.html', posts=sorted_posts, current_sort=sort_by)

@app.route('/post/<int:post_id>')
def post(post_id):
    post_obj = next((p for p in posts if p['id'] == post_id), None)
    if post_obj is None:
        abort(404)
    post_obj['views'] += 1 # Increment views
    return render_template('post.html', post=post_obj) # Removed redundant placeholders

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    global next_post_id
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = {
            'id': next_post_id, 
            'title': title, 
            'content': content,
            'likes': 0,
            'views': 0
        }
        posts.append(new_post)
        next_post_id += 1
        return redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/like_post/<int:post_id>')
def like_post(post_id):
    post_obj = next((p for p in posts if p['id'] == post_id), None)
    if post_obj is None:
        abort(404)
    post_obj['likes'] += 1
    return redirect(url_for('post', post_id=post_id))

if __name__ == '__main__':
    app.run(debug=True)
