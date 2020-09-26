
import json
from time import time
import hashlib
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []


        self.new_block(proof=100,previous_hash=1)

    def proof_of_work(self,last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0

        while self.valid_proof(last_proof,proof) is False:
            proof+=1

        return proof

    @staticmethod
    def valid_proof(last_proof,proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexgidest()

        return guess_hash[:-4] == "0000"

    def new_block(self,proof,previous_hash=None):
        """
        Create a new Block in Blockchein
        :param proof <int> The proof given by the Proof of work algorithm
        :param previous_hash <str> Hash of the previous Block
        :return <dict> New block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transaction
        self.current_transaction = []

        self.chain.append(block)

        return block

    def new_transaction(self,sender,recipient,amount):
        """

        Creates a new transaction to go into the next mined Block
        :param sender <str> Address of the Sender
        :param recipient <str> Address of the Recipient
        :param amount <int> Amount
        :return <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).nextdigest()

    @property
    def last_block(self):
        return self.chain[-1]
