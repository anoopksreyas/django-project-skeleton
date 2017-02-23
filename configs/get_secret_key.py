import os, binascii

def get_secret_key():
     '''
     Returns a random string in-order to replace SECURITY_KEY in project's settings.py
     '''
     print(binascii.hexlify(os.urandom(24)))
     
if __name__ == '__main__':
     get_secret_key()
