
from flask import Flask, request, jsonify

from blockchain import Blockchain

# Creating a Web App
app = Flask(__name__)
app.secret_key = "blockchain-QmUWfZSo9YWNqHx5GYrGXpGJZBok5KDB7Q4JVgkub5JHQH"

# Initialization
@app.before_first_request
def initialization():
    Blockchain.initialize()

# Creating new transaction
@app.route('/api/create_transaction', methods = ['POST'])
def add_transaction():
    if request.is_json:
        IpfsHash = Blockchain.create_txn(txn_data = request.get_json())

        response = {
            'message': 'Data will be added to Blockchain',
            'IpfsHash': IpfsHash
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'No json received'
        }
        return jsonify(response), 400

# Getting transaction or block from Blockchain
@app.route('/api/get_by_hash/<IpfsHash>/', methods = ['GET'])
def get_by_hash(IpfsHash):
    response = Blockchain.get_by_hash(IpfsHash)
    return response.json()

# Getting the Transactions that have not been included in a block
@app.route('/api/get_transactions', methods = ['GET'])
def get_data():
    response = {
        'data': Blockchain.data,
        'length': len(Blockchain.data)
    }
    return jsonify(response), 200

# Getting the Full Blockchain
@app.route('/api/get_chain', methods = ['GET'])
def get_chain():
    response = {
        'chain': Blockchain.chain,
        'length': len(Blockchain.chain)
    }
    return jsonify(response), 200


# Node Communication
# Creating new Blockchain-block
@app.route('/api/create_block', methods = ['GET'])
def create_block():
    block = Blockchain.create_block(nonce=0, previous_hash=Blockchain.chain[-1]['hexdigest'], data=Blockchain.data)

    return jsonify({
        'message': 'New block will be created'
    }), 200

# Accept Transaction
@app.route('/api/post_txn/<IpfsHash>/', methods = ['GET'])
def post_txn(IpfsHash):
    if IpfsHash not in Blockchain.data:
        Blockchain.add_data(IpfsHash)

    return jsonify({
        'message': 'Transactional-data received successfully'
    }), 200

# Accept Block
@app.route('/api/post_block/<hexdigest>/<IpfsHash>/', methods = ['GET'])
def post_block(hexdigest, IpfsHash):
    block = {'hexdigest':hexdigest,'IpfsHash':IpfsHash}
    if block not in Blockchain.chain:
        Blockchain.add_block(block)

    return jsonify({
        'message': 'New block received successfully'
    }), 200

# Checking if the Blockchain is valid
@app.route('/api/is_blockchain_valid', methods = ['GET'])
def is_valid():
    is_valid = Blockchain.is_chain_valid()
    if is_valid:
        message = 'All good. The Blockchain is valid.'
    else:
        message = 'Problem. The Blockchain is not valid.'

    return jsonify({
            'message': message
    }), 200


# Running the app
if __name__ == '__main__':
	app.run(port = 8000)

'''
# Connecting new node
@app.route('/api/connect_node', methos = ['GET'])
def connect_node():
    node = request.remote_addr
    if node in Blockchain.nodes:
        response = {
            'message': 'You are part of blockchain'
        }
        return jsonify(response), 200
    else:
        Blockchain.nodes.add(node)
        return True

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = Blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            'message': 'The nodes had different chains so the chain was replaced by the longest one.',
            'new_chain': Blockchain.chain
        }
    else:
        response = {
            'message': 'All good. The chain is the largest one.',
            'actual_chain': Blockchain.chain
        }
    return jsonify(response), 200
'''
