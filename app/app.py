from flask import request, Flask, jsonify

app = Flask(__name__)

#in-memory data, this is mimicking a database
accounts = {
    '1234':{'balance': 2000},
    '5678':{'balance': 500},
}

# get_balance
# description: GET request for account balance given account_id
# returns: balance in account
@app.route('/accounts/<account_id>', methods=['GET'])
def get_balance(account_id):
    if account_id not in accounts:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({'balance': accounts[account_id]['balance']})

# deposit
# description: POST request for depositing a given amount {"amount":int}
# returns: deposit message
@app.route('/accounts/<account_id>/deposit', methods=['POST'])
def deposit(account_id):
    if account_id not in accounts:
        return jsonify({'error': 'Account not found'}), 404
    
    data = request.get_json()
    amount = data.get('amount')
    
    if amount is None:
        return jsonify({'error': 'Missing amount parameter'}), 400
    
    if amount > 10000:
        return jsonify({'error': 'Deposit amount exceeds maximum limit of $10,000'}), 400

    accounts[account_id]['balance'] += amount
    return jsonify({'message': 'Deposit successful!'})

# withdraw
# description: POST request for withdrawing from account, if allowed
# returns: withdrawal message
@app.route('/accounts/<account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    if account_id not in accounts:
        return jsonify({'error': 'Account not found'}), 404
    
    data = request.get_json()
    amount = data.get('amount')
    if amount is None:
        return jsonify({'error': 'Missing amount parameter'}), 400
    
    if accounts[account_id]['balance'] - amount < 100:
        return jsonify({'error':'Insufficient balance'}), 400

    if amount > accounts[account_id]['balance'] * 0.9:
        return jsonify({'error': 'Withdrawal amount exceeds limit of 90% of account balance'}), 400

    accounts[account_id]['balance'] -= amount
    return jsonify({'message': 'Withdrawal successful'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
