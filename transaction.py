import hashlib
import codecs
import binascii

class Transaction():

    '''Transaction class
- During initialization, the sender, recipient and amount parameters are passed and stored at the instance level.

- There is a transaction hash calculation method. The hash is calculated using the SHA256 algorithm, the parameter for which is the concatenation of the
above parameters in appropriate order.'''

    sender = '0'
    recipient = '0'
    amount = '0'
    signature = '0'
    pubkey = '0'

    def __init__(self, s, r, a):
        self.sender = s
        self.recipient = r
        self.amount = a

    def txHashCalc(self):
        __txhex = self.sender + self.recipient + self.amount
        __txhash = hashlib.sha256(__txhex.encode()).digest()
        __txHashHex = codecs.decode(binascii.hexlify(__txhash))
        return __txHashHex

class CoinbaseTransaction(Transaction):

    '''serves as the reward to the miner'''

    def __init__(self, r, a):
        self.sender = '00000000000000000000000000000000000'
        self.recipient = r
        self.amount = a

    def txHashCalc(self):
        __txhex = self.sender + self.recipient + self.amount
        __txhash = hashlib.sha256(__txhex.encode()).digest()
        __txHashHex = codecs.decode(binascii.hexlify(__txhash))
        return __txHashHex


if __name__ == '__main__':
    tx = Transaction('1to4yvjbUSJvUYKJ6JertB7nUBJvJEQXG', '1GAehh7TsJAHuUAeKZcXf5CnwuGuGgyX2S', '0001')
    print(tx.txHashCalc())
    cbtx = CoinbaseTransaction('1NfCCZ5DY2GQjJR6SzsDfGgy3mGDYjDKuJ', '00000050')
