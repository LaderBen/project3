from app.db.models import User, Song
from flask_login import current_user

def test_register_user_function(client):
    #get csrf token
    token = str(client.get('/register').data)
    start = token.find('name="csrf_token" type="hidden" value="')+len('name="csrf_token" type="hidden" value="')
    end = token.find('">\\n        \\n            \\n\\n    \\n    \\n        \\n    \\n\\n    \\n\\n    \\n    \\n    \\n    \\n    \\n\\n    <div class="mb-3 required"><label class="form-label" for="email">Email Address</label>\\n                        <input class="form-control" id="email"')
    token = token[start:end]
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
    token = str(client.get('/register').data)
    start = token.find('name="csrf_token" type="hidden" value="') + len('name="csrf_token" type="hidden" value="')
    end = token.find(
        '">\\n        \\n            \\n\\n    \\n    \\n        \\n    \\n\\n    \\n\\n    \\n    \\n    \\n    \\n    \\n\\n    <div class="mb-3 required"><label class="form-label" for="email">Email Address</label>\\n                        <input class="form-control" id="email"')
    token = token[start:end]
    data = {
        'email': 'test@test.com',
        'password': '123456',
        'confirm': '123456',
        'csrf_token': token
    }
    client.post('/register', data=data)
    # get csrf token
    token = str(client.get('/login').data)
    start = token.find('name="csrf_token" type="hidden" value="') + len('name="csrf_token" type="hidden" value="')
    end = token.find(
        '">\\n        \\n            \\n\\n    \\n    \\n        \\n    \\n\\n    \\n\\n    \\n    \\n    \\n    \\n    \\n\\n    <div class="mb-3 required"><label class="form-label" for="email">Email Address</label>\\n                        <input class="form-control" id="email"')
    token = token[start:end]
    data = {
        'email': 'test@test.com',
        'password': '123456',
        'csrf_token': token
    }
    response = client.post('/login', data=data)
    #once login success it will redirect to /dashboard
    assert response.status_code == 302
    assert b'/dashboard' in response.data
