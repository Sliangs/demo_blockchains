import hashlib
import json
from time import time

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        #create GENESIS block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        """
        Create a new block in Blockchain
        :param proof:<int>The proof by the proof of work Algorithm
        :param previous_hash:(Optional)<str>Hash of the Previous Block
        :return:<dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        #reset the current list of transactions
        self.current_transactions=[]
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions
        """
        Creates a new transaction to go into the next mined block.
        :param sender:<str> Address of the sender
        :param recipient:<str> Address of the Recipient
        :param amount:<int> Amount

        :return:<int>The Index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index']+1

    def proof_of_work(self, last_proof):
        """
        simple proof of work algor, find a number p' such that has (pp') contains 4 leading zeroes, where
        p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof



    @staticmethod

    def hash(block):
        # Hashes a Block
        '''
        Creates a SHA-256 Hash of a Block
        :param block:<dict> Block
        :return:<str>
        '''
        #We must make sure the dictionary is ordered or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_proof(last_proof, proof):
        """
        Validates the proof: does hash(last_proof, proof) contain 4 leading zeroes?
        :param proof: <int> previous proof
        :return: <bool> true if correct, false if not
        """
        guess = f'{last_proof}{proof}'.encoded()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'


    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]
