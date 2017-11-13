import os

from Crypto.PublicKey import RSA
from OpenSSL import crypto
from playground.common.CipherUtil import *

from playground.common.CipherUtil import *
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa

root = os.path.dirname(os.path.abspath(__file__))
path = os.path.dirname(os.path.dirname(root))

def getPrivateKeyForAddr():
    # Enter the location of the Private key as per the location of the system
    with open(path + "/certs/private_key")as fp:
        private_key_user = fp.read()
    fp.close()

    return private_key_user

def getCertForAddr():
    certs = []
    with open(path + "/certs/signed.cert") as fp:
        certs.append(str.encode(fp.read()))
    fp.close()
    with open(path + "/certs/csr_file") as fp:
        certs.append(str.encode(fp.read()))
    fp.close()

    return certs

def getCert():
    with open(path + "/certs/signed.cert", "rb") as fp:
        cert = fp.read()

    return cert


def getRootCert():

    with open(path + "/certs/root.crt") as fp:
        root_cert = fp.read()

    return root_cert

#print(root)
#print(path)
#print(getPrivateKeyForAddr())
def main():
    # Loading a Certificate
    # rootCertificate = loadCertFromFile("root.crt")
    # Get issuer details
    # Returns a dictionary, parse it to get individual fields
    # rootCertificateIssuerDetails = getCertIssuer(rootCertificate)

    # Get subject details
    # Returns a dictionary, parse it to get individual fields
    # rootCertificateSubjectDetails = getCertSubject(rootCertificate)
    '''cert = x509.load_pem_x509_certificate(getCert(), default_backend())
    public_key = cert.public_key()
    print(isinstance(public_key, rsa.RSAPublicKey))'''


    # cert = getCertForAddr()
    # C_crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert[0])
    # public_key = cert.public_key()
    # iv = os.urandom(16)
    # print(isinstance(public_key, rsa.RSAPublicKey))
    # print(getCertIssuer(cert))
    # print(getCertSubject(cert))
    # enc = CIPHER_AES128_CBC(public_key, iv)
    # ciphertext = enc.encrypt("test message")
    # print(ciphertext)
    crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, getCert())
    pubKeyObject = crtObj.get_pubkey()
    pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM, pubKeyObject)
    print(pubKeyString)
    PKs = b'hello'
    key = RSA.importKey(pubKeyString)
    print(key.can_encrypt())
    print(key.can_sign())
    print(key.has_private())
    public_key = key.publickey()
    enc_data = public_key.encrypt(PKs,32)
    print(type(enc_data))
    print(enc_data[0])
    private_key=RSA.importKey(getPrivateKeyForAddr())
    dec_data=private_key.decrypt(enc_data[0])
    print(dec_data)

if __name__ == "__main__":
    main()





