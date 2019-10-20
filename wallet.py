import binascii
import ecdsa
import hashlib
import base58
import codecs

class Wallet():

    '''A Wallet class 
    - Converts the private key to WIF.
    The private key has the form of a number presented in hex with the size of 32 bytes.

    - Generates new private key using the ECDSA algorithm and the curve used in Bitcoin

    - Generates a public key from a private key for verification in the
    string format
    - From a private key to get a public address, which has the form of a Bitcoin
    address from mainnet.
    - Sign the message with the private key, which is passed by the parameter (as
    well as the message) to the method. Returns the signature and public key for verification.'''

    b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    # def __init__(self):
        # self.__private_keys = [] # Don't think its needed here

    def GenPrivKey(self):
        new_priv_key = binascii.hexlify(ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).to_string()).decode('ascii').upper()
        # self.__private_keys.append(new_priv_key)
        return new_priv_key

    def base58Encode(self, num):
        result = ''
        num = int(num)
        while num > 0:
            result = self.b58[num % 58] + result
            num = num // 58
        return result

    def base58Decode(self, __str):
        l = []
        for c in self.b58:
            l.append(c)
        res = 0
        for __char in __str:
            res = res * 58 + l.index(__char)
        return hex(res)

    def countChars(self, __str, char):
        number = 0
        for c in __str:
            if (c == char):
                number += 1
            else:
                break
        return number

    def base58CheckEncode(self, __version, __payload):
        __step1 = __version + __payload
        __checksum = hashlib.sha256(hashlib.sha256(bytes.fromhex(__step1)).digest()).hexdigest()[0:8]
        __step2 = __step1 + __checksum
        __final = '1' * (self.countChars(__step2, '0') // 2) + self.base58Encode(int(__step2, 16)) #__final = base58.b58encode_int(int(__step4, 16)).decode()
        return __final

    def privateKeyToPublicKey(self, __privKey):
        __sk = ecdsa.SigningKey.from_string(bytes.fromhex(__privKey), curve=ecdsa.SECP256k1)
        vk = __sk.get_verifying_key()
        return ('04' + vk.to_string().hex()).upper()

    def pubKeyToAddress(self, pubKey):
        __ripemd160 = hashlib.new('ripemd160')
        __ripemd160.update(hashlib.sha256(bytes.fromhex(pubKey)).digest())
        __protoAddress = __ripemd160.hexdigest()
        return self.base58CheckEncode('00', __protoAddress)
        # return base58.b58encode_check('00', __protoAddress)

    def signMessage(self, __privKey, __message):
        __sk = ecdsa.SigningKey.from_string(bytes.fromhex(__privKey), curve=ecdsa.SECP256k1)
        signature = __sk.sign(__message.encode('utf-8'))
        vk = __sk.get_verifying_key()
        # pubkey = self.privateKeyToPublicKey(__privKey)
        # vkt = ecdsa.VerifyingKey.from_string(binascii.unhexlify(pubkey[2:]), curve=ecdsa.SECP256k1)
        
        # print('vk = ', codecs.decode(binascii.hexlify(vk.to_string())), '\npubkey = ', pubkey)
        # print('signature = ', signature)
        # return vkt.verify(signature, 'ba61b8ff81318fc59a59b37dce253ff9e80caf330ac4afa207ad3334583cece7'.encode('utf-8'))
        return signature, vk.to_string().hex().upper()
    
if __name__ == '__main__':
    wallet = Wallet()
    # print(wallet.GenPrivKey())
    print(wallet.base58CheckEncode('80', '0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D'))
    # print(wallet.privateKeyToPublicKey('23D1662734D1741BF5CAFFABF33A2829F2D5A658CA02CA40380CE96813145101'))
    # print(wallet.pubKeyToAddress(wallet.privateKeyToPublicKey('0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D')))
    # print(wallet.signMessage('23D1662734D1741BF5CAFFABF33A2829F2D5A658CA02CA40380CE96813145101', 'ba61b8ff81318fc59a59b37dce253ff9e80caf330ac4afa207ad3334583cece7'))

    #sender
    #prk 0C28FCA386C7A227600B2FE50B7CAE11EC86D3BF1FBE471BE89827E19D72AA1D
    #pbk 04D0DE0AAEAEFAD02B8BDC8A01A1B8B11C696BD3D66A2C5F10780D95B7DF42645CD85228A6FB29940E858E7E55842AE2BD115D1ED7CC0E82D934E929C97648CB0A
    #add 1GAehh7TsJAHuUAeKZcXf5CnwuGuGgyX2S
    #recipient
    #prk 7f83b228d628e9f49fc64457149039951f7982065fea88f7a31e483b865040f1
    #pbk 04C39780790B9BA856FDF3E7B24F70BFBEACD4B9F62A0B38B1D1EDCD7DCB857BAE1B9FCA6828994A0E1D3FAF2C77FB0B3E446F7F7BA841426EA2B617104945935D
    #add 1to4yvjbUSJvUYKJ6JertB7nUBJvJEQXG
    #miner
    #prk 23D1662734D1741BF5CAFFABF33A2829F2D5A658CA02CA40380CE96813145101
    #pbk 040E44B5C4C47AB5017BD0E444B57997F5C1F0C1A56401051EE5CC1FC14F8BEBF2E16985CE4E33F7056C1F4C16D91D43073D4E040EC982F9796F1E491D01F3F0DB
    #add 1NfCCZ5DY2GQjJR6SzsDfGgy3mGDYjDKuJ
