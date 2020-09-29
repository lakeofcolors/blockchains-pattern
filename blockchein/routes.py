from flask import Blueprint, jsonify, request
import json
from .core import Blockchain
from uuid import uuid4

blockchain = Blueprint('blockchein', __name__)
blockchain_object = Blockchain()

node_identificator = str(uuid4()).replace('-','')

@blockchain.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain_object.last_block


    last_proof = last_block['proof']

    proof = blockchain_object.proof_of_work(last_proof)

    blockchain_object.new_transaction(
        sender="0",
        recipient=node_identificator,
        amount=1,
    )


    previous_hash = blockchain_object.hash(last_block)
    block = blockchain_object.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@blockchain.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender','recipient','amount']

    if not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain_object.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message':f'Transaction will be added to block {index}'}

    return jsonify(response), 201

@blockchain.route('/chain', methods=['GET'])
def full_chain():

    response = {
        'chain': blockchain_object.chain,
        'lenght': len(blockchain_object.chain)
    }

    return jsonify(response), 200

@blockchain.route('/node/register',methods=['POST'])
def register_node():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return 'Error:Suply a valid list of nodes', 400

    for node in nodes:
        blockchain_object.register_node(node)

    response = {
        "message":"Node have been added",
        "total_nodes": list(blockchain_object.nodes)
    }

    return jsonify(response), 201

@blockchain.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain_object.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain_object.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain_object.chain
        }

    return jsonify(response), 200
