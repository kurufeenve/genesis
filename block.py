from merkle import *
from tx_validator import *
from serializer import Deserializer
import json

class Block():

    '''meneging blocks'''

    timestamp = '0'
    nonce = '0'
    previous_hash = '0'
    transactions = '0'
    blockhash = '0'
    block_root = '0'

    def __init__(self, timestamp, previous_hash, transactions):
        self.timestamp = timestamp
        self.nonce = 0
        self.previous_hash = previous_hash
        self.transactions = transactions

    def blockHashCalc(self, genesis):
        if self.txValidator(self.transactions):
            root = merkle_root(self.transactions)
            # print('self.timestamp = ', type(self.timestamp), '\nself.nonce = ', self.nonce,
            #     '\nself.previous_hash = ', type(self.previous_hash), '\nroot = ', type(root))
            __preHash = str(self.timestamp) + str(self.nonce) + str(self.previous_hash) + str(root)
            # print('__prehash = ', __preHash)
            blockHash = hashlib.sha256(hashlib.sha256(__preHash.encode()).digest()).hexdigest()
            self.blockhash = blockHash
            self.block_root = root
            return blockHash, root
        elif genesis == 1:
            tx = Deserializer.deserialize(Deserializer, self.transactions[0])
            tx.sender = '00000000000000000000000000000000'
            # print('txHash = ', tx.txHashCalc().encode('utf-8'), '\ntxpubkey = ', tx.pubkey, '\nsignature = ', tx.signature)
            if (Validator.addrVal(Validator, tx.recipient)) and Validator.signatureVal(Validator, tx.txHashCalc().encode('utf-8'), tx.pubkey, tx.signature):
                root = merkle_root(self.transactions)
                # print('root = ', root)
                __preHash = str(self.timestamp) + str(self.nonce) + str(self.previous_hash) + str(root)
                # print('pre hash = ', __preHash.encode())
                blockHash = hashlib.sha256(hashlib.sha256(__preHash.encode()).digest()).hexdigest()
                # print('blockHash = ', blockHash)
                self.blockhash = blockHash
                self.block_root = root
                return blockHash, root
            else:
                return False
        else:
            print('one or more transactions are compromised')
            return False

    def txValidator(self, transactions):

        for stx in transactions:
            tx = Deserializer.deserialize(Deserializer, stx)
            if stx[4:40] == '0' * 36 and not Validator.addrVal(Validator, tx.recipient):
                return True
            elif not Validator.addrVal(Validator, tx.sender) or not Validator.addrVal(Validator, tx.recipient) or not Validator.senderAddrVal(Validator, tx.pubkey, tx.sender):
                break
            elif not Validator.signatureVal(Validator, tx.txHashCalc().encode('utf-8'), tx.pubkey, tx.signature):
                break
            else:
                return True
        return False        

    def mining(self, complexity):
        print('Du u know da way?????')


#timestamp + nonce + previous_hash + merkle tree
