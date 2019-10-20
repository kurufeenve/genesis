import codecs
from wallet import *

class Validator():

    '''Validator class has methods that provide verification of the transaction:

- For availability of addresses

- To verify that the sender's address belongs to the public key by obtaining
the bitcoin format from the attached public key and comparing with the sender's address attached in the transaction

- The validity of the signature by verifying the attached signature, the public key, and the newly computed transaction hash using its corresponding
method.'''

    def addrVal(self, address):
        hexaddr = codecs.decode(binascii.hexlify(base58.b58decode(address)), 'ascii')
        checksum = hexaddr[-8:]
        checkchecksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(hexaddr[:-8])).digest()).hexdigest()[0:8]
        if checksum != checkchecksum:
            return False
        elif len(address) < 26 or len(address) > 35:
            return False
        elif address[0] != '1' and address[0] != '3':
            return False
        else:
            return True

    def senderAddrVal(self, pubkey, sender):
        wallet = Wallet()
        senderAddressFromPubkey = wallet.pubKeyToAddress(pubkey)
        if sender != senderAddressFromPubkey:
            return False
        else:
            return True
    #@staticmethod
    def signatureVal(self, message, pubkey, signature): #message should be in bytes in utf-8 and signature in bytes
        # assert isinstance(message, str) and isinstance(signature, str), "message should be in bytes in utf-8 and signature in bytes"
        try:
            # print('>>>>>>>>>sigVal', '\nmessage = ', message, '\npubkey = ', pubkey, '\nsignature = ', signature, '\n>>>>>>>>>>')
            vk = ecdsa.VerifyingKey.from_string(binascii.unhexlify(pubkey[2:]), curve=ecdsa.SECP256k1)
            return vk.verify(signature, message)
        except:
            print('Warum?')
            return False

if __name__ == '__main__':
    val = Validator()
    # print(val.addrVal('1to4yvjbUSJvUYKJ6JertB7nUBJvJEQXG'))
    w = Wallet()
    signature, pk = w.signMessage('0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D', 'message')
    print(val.signatureVal('message'.encode(), '04D0DE0AAEAEFAD02B8BDC8A01A1B8B11C696BD3D66A2C5F10780D95B7DF42645CD85228A6FB29940E858E7E55842AE2BD115D1ED7CC0E82D934E929C97648CB0A', signature))
