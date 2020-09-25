#!/usr/bin/env python
import json
from time import time
import hashlib

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

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
        pass

    @property
    def last_block(self):
        pass
