from transaction import *
from tx_validator import *
from wallet import *

class Serializer():

    def serialize(self, tx):
        stx = tx.amount + '0' * (35 - len(tx.sender)) + tx.sender + '0' * (35 - len(tx.recipient)) + tx.recipient + tx.pubkey + tx.signature.upper()
        print(len(tx.amount))
        print(len(stx[202:]))
        return stx

class Deserializer():

    def deserialize(self, stx):
        amount = stx[:4]
        sender = stx[4:39].strip('0')
        recipient = stx[39:74].strip('0')
        pubkey = '04' + stx[74:202]
        signature = binascii.unhexlify(stx[202:])
        tx = Transaction(sender, recipient, amount)
        tx.pubkey = pubkey
        tx.signature = signature
        return tx
        
if __name__ == '__main__':
    tx = Transaction('1to4yvjbUSJvUYKJ6JertB7nUBJvJEQXG', '1GAehh7TsJAHuUAeKZcXf5CnwuGuGgyX2S', '0001')
    txHash = tx.txHashCalc()
    tx.signature, tx.pubkey = Wallet.signMessage(Wallet, '7f83b228d628e9f49fc64457149039951f7982065fea88f7a31e483b865040f1', txHash)
    tx.signature = codecs.decode(binascii.hexlify(tx.signature))
    print(Serializer.serialize(Serializer, tx))
