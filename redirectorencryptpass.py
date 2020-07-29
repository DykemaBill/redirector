import sys
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet

# Encyption
def passencrypt(mypassword):
    if mypassword:
        # Generate key
        key = Fernet.generate_key()
        # Decoded encryption key to be stored
        keyDecoded = key.decode("utf-8")
        print ("Here is your decoded key to be stored: " + str(keyDecoded))
        # Set key
        encryptKey = Fernet(key)
        # Encrypt password from byte form with str.encode
        encryptPass = encryptKey.encrypt(str.encode(mypassword))
        # Decode encrypted password to string form to be stored
        encryptPassDecoded = encryptPass.decode("utf-8")
        print ("Here is your encrypted password be stored: " + str(encryptPassDecoded))

        # Take key from stored form and convert it back to byte form
        keyRecovered = keyDecoded.encode("utf-8")
        print ("Here is your original key: " + str(keyRecovered))
        encryptKeyRecovered = Fernet(keyRecovered)
        # Using recovered key unencrypt stored password
        encryptPassEncode = encryptPassDecoded.encode("utf-8")
        print ("Here is your password before unencrypting it: " + str(encryptPassEncode))
        originalPassByte = encryptKeyRecovered.decrypt(encryptPassEncode)
        originalPass = originalPassByte.decode("utf-8")
        print ("Here is your password after unencrypting: " + str(originalPass))
    else:
        print ("You did not give me a password to encrypt!")

# Get command line arguments
if __name__ == "__main__":
    if len(sys.argv) == 2:
        passencrypt(sys.argv[1])
    else:
        print ("Syntax: " + sys.argv[0] + " [password]")