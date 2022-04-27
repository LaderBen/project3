def test_register_user_function(client):
    data = {
        'email': 'test@test.com',
        'password': '123456',
        'confirm': '123456'
    }
    response = client.post('/register', data=data)
    assert b'Congratulations, you are now a registered user!' in response.data