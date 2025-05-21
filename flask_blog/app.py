from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Temporary in-memory list to store blog posts
posts = []
next_post_id = 1

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        abort(404)
    return render_template('post.html', post=post, post_title_placeholder=post['title'], post_content_placeholder=post['content'])

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    global next_post_id
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = {'id': next_post_id, 'title': title, 'content': content}
        posts.append(new_post)
        next_post_id += 1
        return redirect(url_for('index'))
    return render_template('create_post.html')

if __name__ == '__main__':
    app.run(debug=True)
