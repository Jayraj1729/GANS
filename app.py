from flask import Flask, redirect, request, session, render_template
from github import Github
import scanner
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'access_token' not in session:
        return redirect('/login')
    repo_url = request.args.get('repo_url')
    if repo_url:
        scan_results = scanner.scan_repository(repo_url)
        session['scan_results'] = scan_results
    return redirect('/dashboard')
    return render_template('dashboard.html', scan_results=scan_results)
#
@app.route('/login')
def login():
    github = Github()
    redirect_uri = request.url_root + 'callback'
    authorization_url, state = github.authorization_url(client_id=os.environ['GITHUB_CLIENT_ID'], redirect_uri=redirect_uri, scope=['repo'])
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    state = session.pop('oauth_state', None)
    if state is None or state != request.args.get('state'):
        return redirect('/')
    github = Github()
    redirect_uri = request.url_root + 'callback'
    token = github.get_access_token(client_id=os.environ['GITHUB_CLIENT_ID'], client_secret=os.environ['GITHUB_CLIENT_SECRET'], code=request.args.get('code'), redirect_uri=redirect_uri, state=state)
    session['access_token'] = token
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)

