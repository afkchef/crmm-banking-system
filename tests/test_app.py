import requests

def test_get_balance_account():
    response = requests.get("http://0.0.0.0:5000/accounts/1234")
    assert response.status_code == 200
    assert response.json() == {"balance":2000}

def test_get_balance_no_account():
    response = requests.get("http://0.0.0.0:5000/accounts/9999")
    assert response.status_code == 404
    assert response.json() == {"error":"Account not found"}

def test_deposit_success():
    payload = {'amount': 1000}
    response = requests.post('http://0.0.0.0:5000/accounts/1234/deposit', json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == 'Deposit successful!'
    
    # Check user's balance has been updated
    response = requests.get('http://0.0.0.0:5000/accounts/1234')
    assert response.status_code == 200
    assert response.json()['balance'] == 3000

def test_deposit_too_much():
    payload = {'amount': 10001}
    response = requests.post('http://0.0.0.0:5000/accounts/1234/deposit', json=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'Deposit amount exceeds maximum limit of $10,000'


def test_withdraw_success():
    payload = {'amount': 1000}
    response = requests.post('http://0.0.0.0:5000/accounts/1234/withdraw', json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == 'Withdrawal successful'
    
    # Check that the user's balance has been updated correctly
    response = requests.get('http://0.0.0.0:5000/accounts/1234')
    assert response.status_code == 200
    assert response.json()['balance'] == 2000

def test_withdraw_over_balance():
    payload = {'amount': 2001}
    response = requests.post('http://0.0.0.0:5000/accounts/1234/withdraw', json=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'Insufficient balance'
    
    # Check that the user's balance has not been updated
    response = requests.get('http://0.0.0.0:5000/accounts/1234')
    assert response.status_code == 200
    assert response.json()['balance'] == 2000

def test_withdraw_90_percent():
    payload = {'amount': 1801}
    response = requests.post('http://0.0.0.0:5000/accounts/1234/withdraw', json=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'Withdrawal amount exceeds limit of 90% of account balance'
    
    # Check that the user's balance has not been updated
    response = requests.get('http://0.0.0.0:5000/accounts/1234')
    assert response.status_code == 200
    assert response.json()['balance'] == 2000

def test_withdraw_account_less_than_100():
    payload = {'amount': 1901}
    response = requests.post('http://0.0.0.0:5000/accounts/1234/withdraw', json=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'Insufficient balance'
    
    # Check that the user's balance has not been updated
    response = requests.get('http://0.0.0.0:5000/accounts/1234')
    assert response.status_code == 200
    assert response.json()['balance'] == 2000
