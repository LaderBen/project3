from app.db.models import User, Song
from app import config

from pathlib import Path
import os
import time
from flask_login import current_user

def test_register_user_function(client):
    #get csrf token
    token = get_token('/register', client)
    data = {
        'email': 'test@test.com',
        'password': '123456',
        'confirm': '123456',
        'csrf_token': token
    }
    response = client.post('/register', data=data)
    user = User.query.filter_by(email='test@test.com').first()
    assert response.status_code == 301
    assert user.email == 'test@test.com'

def test_user_login_function(client):
    #register a user
    # get csrf token
    token = get_token('/register', client)
    data = {
        'email': 'test@test.com',
        'password': '123456',
        'confirm': '123456',
        'csrf_token': token
    }
    client.post('/register', data=data)
    #login
    # get csrf token
    token = get_token('/login', client)

    data = {
        'email': 'test@test.com',
        'password': '123456',
        'csrf_token': token
    }
    response = client.post('/login', data=data)
    #once login success it will redirect to /dashboard
    assert response.status_code == 302
    assert b'/dashboard' in response.data

def test_user_file_upload(client):
    # register a user
    # get csrf token
    token = get_token('/register', client)
    data = {
        'email': 'test@test.com',
        'password': '123456',
        'confirm': '123456',
        'csrf_token': token
    }
    client.post('/register', data=data)
    # login
    # get csrf token
    token = get_token('/login', client)
    data = {
        'email': 'test@test.com',
        'password': '123456',
        'csrf_token': token
    }
    client.post('/login', data=data)
    #upload file
    root = Path(__file__).parent.parent
    test_file = root / 'tests'/'music.csv'
    upload_dir = root / 'app' / 'uploads' / 'music.csv'
    if os.path.exists(upload_dir):
        os.remove(upload_dir)
    assert not os.path.exists(upload_dir)
    assert os.path.exists(test_file)
    token = str(client.get('/songs/upload').data)
    start = token.find('name="csrf_token" type="hidden" value="') + len('name="csrf_token" type="hidden" value="')
    end = token.find(
        '">\\n        \\n            \\n\\n    \\n    \\n        \\n    \\n\\n    \\n\\n    \\n    \\n    \\n    \\n    \\n\\n    <div class="mb-3 required"><label class="form-label" for="file">File</label>')
    token = token[start:end]
    data = {
        'csrf_token': token,
        'file': test_file.open('rb')
    }
    client.post('/songs/upload',data = data)
    time.sleep(1)
    upload_dir = root / 'app' / 'uploads' / 'home_runner_work_project3_project3_tests_music.csv'
    assert os.path.exists(upload_dir)
    os.remove(upload_dir)




def get_token(url, client):
    token = str(client.get(url).data)
    start = token.find('name="csrf_token" type="hidden" value="') + len('name="csrf_token" type="hidden" value="')
    end = token.find(
        '">\\n        \\n            \\n\\n    \\n    \\n        \\n    \\n\\n    \\n\\n    \\n    \\n    \\n    \\n    \\n\\n    <div class="mb-3 required"><label class="form-label" for="email">Email Address</label>\\n                        <input class="form-control" id="email"')
    token = token[start:end]
    return token